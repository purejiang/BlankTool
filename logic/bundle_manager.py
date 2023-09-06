# -*-coding:utf-8 -*-

import os
import re
import traceback
import zipfile
from cmd_util.apk_cmd import ApkCMD
from cmd_util.bundle_cmd import BundleCMD
from common.constant import Constant
from utils.file_helper import FileHelper
from utils.jloger import JLogger
from utils.other_util import currentTime, currentTimeNumber

class BundleManager():
    """
    @author: purejiang
    @created: 2022/7/13

    .aab 相关的功能管理

    """

    @classmethod
    def install_aab(cls, aab_path, signer_config, progress_callback):
        apks_path = os.path.join(Constant.Path.INSTALL_CACHE_PATH, "{0}.apks".format(FileHelper.filename(aab_path, False)))
        cls.loger.info("开始安装 aab，时间："+ currentTime())
        try:
            if FileHelper.fileExist(apks_path):
                FileHelper.delFile(apks_path)
            progress_callback(10, "清理输出目录...", "", True)

            
            aab2apks_result = BundleCMD.aab2Apks(Constant.Re.BUNDLETOOL_PATH, aab_path, apks_path, signer_config)
            progress_callback(30, "aab 转 apks...", aab2apks_result[1], aab2apks_result[0])
            if not aab2apks_result[0]:
                return False
            
            
            install_apks_result = BundleCMD.installApks(Constant.Re.BUNDLETOOL_PATH, apks_path)
            progress_callback(70, "安装 apks...", install_apks_result[1], install_apks_result[0])
            if not install_apks_result[0]:
                return False
            return True
        except Exception as e:
            cls.loger.warning(""+traceback.format_exc())
            return False
        
    @classmethod
    def install_apks(cls, apks_file, progress_callback):
        cls.loger.info("开始安装 apks，时间："+ currentTime())
        try:
            progress_callback(30, "安装 apks...", "", True)
            install_apks_result = BundleCMD.installApks(Constant.Re.BUNDLETOOL_PATH, apks_file)
            progress_callback(70, "安装 apks完成", install_apks_result[1], install_apks_result[0])
            if not install_apks_result[0]:
                return False
            return True
        except Exception as e:
            cls.loger.warning(""+traceback.format_exc())
            return False
        
    
    @classmethod
    def apk2aab(cls, apk_file, ver_config, signer_config, progress_callback):
        loger = JLogger(log_name="apk2aab_{0}.log".format(currentTimeNumber()), save_file=True)
        progress_callback(5, "开始初始化转换工具" , "", True)
        md5_name = "{0}_{1}".format(FileHelper.filename(apk_file, False), FileHelper.md5(apk_file))
        output_aab_file = os.path.join(Constant.Path.AAB_CACHE_PATH, "{0}_{1}_{2}.aab".format(md5_name, ver_config["ver_name"], currentTimeNumber()))
        work_space_dir = os.path.join(Constant.Path.AAB_CACHE_PATH, md5_name)
        depack_dir = os.path.join(work_space_dir, "depackage")
        other_dir = os.path.join(work_space_dir, "other")
        compile_zip = os.path.join(other_dir, "compile.zip")
        base_apk = os.path.join(other_dir, "base.apk")
        # aab  项目结构
        aab_project_dir = os.path.join(work_space_dir, "aab_project")
        aab_base_dir = os.path.join(aab_project_dir, "base")
        aab_assets_res_dir = os.path.join(aab_project_dir, "AssetsPackGameRes")
        aab_base_zip = os.path.join(aab_project_dir, "base.zip")
        aab_assets_res_zip = os.path.join(aab_project_dir, "AssetsPackGameRes.zip")

        if FileHelper.fileExist(output_aab_file):
            loger.info("清理已存在的aab文件:"+output_aab_file)
            FileHelper.delFile(output_aab_file)

        if FileHelper.fileExist(work_space_dir):
            loger.info("清理工作空间:"+work_space_dir)
            FileHelper.delFile(work_space_dir)
        
        loger.info("新建工作空间")
        FileHelper.createDir(work_space_dir)
        FileHelper.createDir(aab_project_dir)
        FileHelper.createDir(other_dir)
        progress_callback(15, "初始化转换工具完成" , "", True) 

        # 反编 apk
        depack_result = cls.__depackageApk(apk_file, depack_dir, loger)
        progress_callback(25, "反编 apk完成", depack_result[1], depack_result[0])
        if not depack_result[0]:
            return
        # 获取包名
        package_name = cls.__parsePackage(depack_dir, loger)
        if package_name is None:
            progress_callback(30, "解析包名失败", package_name, False)
            return
        progress_callback(30, "解析包名完成", package_name, True)

        # 编译资源
        compile_result = cls.__compileZip(depack_dir, compile_zip, loger)
        progress_callback(40, "编译资源完成", compile_result[1], compile_result[0])
        if not compile_result[0]:
            return
        
        # 链接资源
        link_result = cls.__linkRes(Constant.Re.ANDROID_JAR_PATH, compile_zip, depack_dir, ver_config, base_apk, loger)
        progress_callback(50, "链接资源完成", link_result[1], link_result[0])
        if not link_result[0]:
            return
        
        # 整理 base 模块
        arrange_apk_result = cls.__arrangeBaseApk(Constant.Re.SMALI_JAR_PATH, base_apk, aab_base_dir, depack_dir, loger)
        progress_callback(60, "整理 base 模块完成", arrange_apk_result[1], arrange_apk_result[0])
        if not arrange_apk_result[0]:
            return
        
        # 整理 assets 模块
        arrange_assets_result = cls.__arrangeAssets(Constant.Re.ANDROID_JAR_PATH, package_name, apk_file, other_dir, aab_base_dir, aab_assets_res_dir, Constant.Aab.ASSETS_RES_MANIFEST, loger)
        progress_callback(60, "整理 assets 模块完成", arrange_assets_result[1], arrange_assets_result[0])
        if not arrange_assets_result[0]:
            return
        
        # aab 构建
        build_bundle_result = cls.__bundleBuild(Constant.Re.BUNDLETOOL_PATH, aab_base_dir, aab_base_zip, aab_assets_res_dir, aab_assets_res_zip, output_aab_file, loger)
        progress_callback(70, "aab 构建完成", build_bundle_result[1], build_bundle_result[0])
        if not build_bundle_result[0]:
            return
        
        # aab 签名
        sign_bundle_result = cls.__signerAab(Constant.Re.JARSIGNER_PATH, output_aab_file, signer_config, loger)
        progress_callback(80, "aab 签名完成", sign_bundle_result[1], sign_bundle_result[0])
        if not sign_bundle_result[0]:
            return
        return True
        
    @classmethod      
    def __depackageApk(cls, apk_file, depack_dir, loger):
        if FileHelper.fileExist(depack_dir):
            FileHelper.delFile(depack_dir)
            loger.info("del file:"+depack_dir)
        result =  ApkCMD.depackage(Constant.Re.APKTOOL_PATH, apk_file, depack_dir, True, False)
        loger.info("cmd:"+result[2])
        return result

    @classmethod
    def __parsePackage(cls, depack_dir, loger):
        try:
            manifest = os.path.join(depack_dir, "AndroidManifest.xml")
            with open(manifest, "r", encoding="utf-8") as file:
                content = file.read()
            # 非贪婪模式，取第一个
            return re.findall("package=\"(.*?)\"", content)[0]
        except Exception as e:
            loger.warning(str(traceback.format_exc()))
            return None
        
    @classmethod
    def __compileZip(cls, depack_dir, zip_path, loger):
        res_path = os.path.join(depack_dir, "res")
        result = BundleCMD.compileZip( res_path, zip_path)
        loger.info("cmd:"+result[2])
        return result
    
    @classmethod
    def __linkRes(cls, android_jar, compile_zip, depack_dir, ver_config, ouput_base_apk, loger):
        manifest = os.path.join(depack_dir, "AndroidManifest.xml")
        result = BundleCMD.linkRes(compile_zip, android_jar, manifest, ver_config["min_ver"], ver_config["tar_ver"], ver_config["compile_ver"], ver_config["ver_code"], ver_config["ver_name"], ouput_base_apk)
        loger.info("cmd:"+result[2])
        return result
    
    @classmethod
    def __arrangeBaseApk(cls, smali_jar, base_apk, aab_base_dir, depack_dir, loger):
        try:
            move_dict = {}
            with zipfile.ZipFile(base_apk, 'a') as zf:
                zf.extractall(aab_base_dir)
            manifest_dir = os.path.join(aab_base_dir, "manifest")
            FileHelper.createDir(manifest_dir)
            # 移动 manifest
            old_manifest = os.path.join(aab_base_dir, "AndroidManifest.xml")
            new_manifest = os.path.join(manifest_dir, "AndroidManifest.xml")
            move_dict[old_manifest] = new_manifest
            # 移动 assets
            old_assets = os.path.join(depack_dir, "assets")
            new_assets = os.path.join(aab_base_dir, "assets")
            move_dict[old_assets] = new_assets
            # 移动 lib
            old_lib = os.path.join(depack_dir, "lib")
            new_lib = os.path.join(aab_base_dir, "lib")
            move_dict[old_lib] = new_lib
            # 移动 其他文件夹到 unknown
            old_unknown = os.path.join(depack_dir, "unknown")
            kotlin = os.path.join(depack_dir, "kotlin")
            meta_inf = os.path.join(depack_dir, "original/META-INF")
            new_kotlin = os.path.join(old_unknown, "kotlin")
            new_meta_inf = os.path.join(old_unknown, "META-INF")


            FileHelper.copyFile(kotlin, new_kotlin)
            FileHelper.copyFile(meta_inf, new_meta_inf)
            for meta_inf_file in FileHelper.getChild(new_meta_inf):
                if FileHelper.filename(meta_inf_file).endswith(".RSA") or FileHelper.filename(meta_inf_file).endswith(".MF")or FileHelper.filename(meta_inf_file).endswith(".SF"):
                    FileHelper.delFile(meta_inf_file)

            # 移动 unknown
            root = os.path.join(aab_base_dir, "root")
            move_dict[old_unknown] = root

            for old, new in move_dict.items():
                if FileHelper.fileExist(old):
                    if FileHelper.isFile(old):
                        FileHelper.moveFile(old, new)
                    else:
                        FileHelper.copyFile(old, new)
                    loger.info("base apk 整理移动：{0} -> {1}".format(old, new))
            # smali 转 dex
            is_success = cls.__smali2dex(smali_jar, depack_dir, aab_base_dir, loger)
            return is_success, "success"
        except Exception as e:
            loger.warning(""+traceback.format_exc())
            return False, None
        
    @classmethod
    def __smali2dex(cls, smali_jar, depacka_dir, aab_base_dir, loger):
        final_result = True
        new_dex = os.path.join(aab_base_dir, "dex")
        os.makedirs(new_dex)
        for file in os.listdir(depacka_dir):
            file_name = os.path.basename(file)
            if not os.path.isfile(file) and "smali" in file_name:
                if "smali_" in file_name:
                    dex_file = os.path.join(
                        new_dex, file_name.split("smali_")[1]+".dex")
                else:
                    dex_file = os.path.join(new_dex, "classes.dex")
                smali2dex_result = BundleCMD.smali2dex(smali_jar, os.path.join(depacka_dir, file), dex_file)
                loger.info("cmd:"+smali2dex_result[2])
                loger.info("result:"+smali2dex_result[1])
                final_result = final_result and smali2dex_result[0]
        return final_result
    
    @classmethod
    def __bundleBuild(cls, bundle_tool, aab_base_dir, aab_base_zip, aab_assets_dir, aab_assets_zip, output_aab, loger):
        zip_txt = ""
        with zipfile.ZipFile(aab_base_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
            for dirpath, dirnames, filenames in os.walk(aab_base_dir):
                fpath = dirpath.replace(aab_base_dir, '')
                fpath = fpath and fpath + os.sep or ''
                for filename in filenames:
                    zf.write(os.path.join(dirpath, filename), fpath+filename)
        zip_txt += aab_base_zip
        if FileHelper.fileExist(aab_assets_dir):
            with zipfile.ZipFile(aab_assets_zip, 'w', zipfile.ZIP_DEFLATED) as zf2:
                for dirpath, dirnames, filenames in os.walk(aab_assets_dir):
                    fpath = dirpath.replace(aab_assets_dir, '')
                    fpath = fpath and fpath + os.sep or ''
                    for filename in filenames:
                        if filename != "resources.pb":
                            zf2.write(os.path.join(
                                dirpath, filename), fpath+filename)
            zip_txt += (","+aab_assets_zip)
        result = BundleCMD.buildBundle(bundle_tool, zip_txt, output_aab)
        loger.info("cmd:"+result[2])
        return result
    
    @classmethod
    def __signerAab(cls, signer_tool, output_aab, signer_config, loger):
        result = BundleCMD.signBundle(signer_tool, output_aab, signer_config.signer_file_path,signer_config.signer_pwd, signer_config.signer_key_pwd, signer_config.signer_alias)
        loger.info("cmd:"+result[2])
        return result
    
    @classmethod
    def __arrangeAssets(cls, android_jar, package_name, apk_file, other_dir, aab_base_dir, aab_assets_res_dir, assets_manifest, loger):
        output_assets_apk = os.path.join(other_dir, "game_res.apk")
        base_assets = os.path.join(aab_base_dir, "assets")
        # base 的 assets 大于150 mb() 则分割资源
        size = os.path.getsize(apk_file) / 1024.0 ** 2

        if size > 150+1024:
            print("apk 过大，无法分割 assets")
            return False,None
        elif size > 150:
            FileHelper.createDir(aab_assets_res_dir)
            new_assets = os.path.join(aab_assets_res_dir, "assets")
            manifest_dir = os.path.join(aab_assets_res_dir, "manifest")
            FileHelper.createDir(new_assets)
            FileHelper.createDir(manifest_dir)

            manifest = os.path.join(aab_assets_res_dir, "AndroidManifest.xml")
            new_manifest = os.path.join(manifest_dir, "AndroidManifest.xml")
            FileHelper.copyFile(assets_manifest, manifest)
            # 将manifest里面的${package_name}替换成包名
            with open(manifest, "r", encoding="utf-8") as file:
                content = file.read()
            with open(manifest, "w", encoding="utf-8") as file:
                file.write(content.replace(
                    r"${applicationId}", package_name))
                
            for file in os.listdir(base_assets):
                old_file = os.path.join(base_assets, file)
                new_file = os.path.join(new_assets, file)
                # 如果是文件夹就移到 切割的assets
                if not FileHelper.isFile(old_file):
                    FileHelper.moveFile(old_file, new_file)
                else:
                    if ".bundle" in os.path.basename(file):
                        FileHelper.moveFile(old_file, new_file)
            result = BundleCMD.linkResByDir(android_jar, manifest, output_assets_apk)
            loger.info("cmd:"+result[2])
            if result[0]:
                with zipfile.ZipFile(output_assets_apk, 'a') as zf:
                    zf.extractall(aab_assets_res_dir)
                FileHelper.moveFile(manifest, new_manifest)
            return result