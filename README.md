# UEFI-Edior辅助工具使用教程（中英双语）


## 一、前期准备（Preparations）
确保电脑已正确安装相关依赖环境（若有），准备好需要修改的BIOS文件。  
Ensure the relevant dependency environment (if any) is properly installed on your computer. Prepare the BIOS file you need to modify.  


## 二、BIOS文件提取（Extracting the BIOS File）
### 2.1 启动软件（Launch the Software）
运行`UEFI-Edior辅助工具`，界面显示“选择BIOS文件并提取”和“执行合并操作”按钮。  
Run the `UEFI-Edior Assistant Tool`. The interface displays two buttons: "选择BIOS文件并提取 (Select BIOS File and Extract)" and "执行合并操作 (Perform Merge Operation)".  

![工具启动界面](https://raw.githubusercontent.com/jhsvip/ue-assist/main/教程/1UI.jpg)  


### 2.2 选择BIOS文件（Select BIOS File）
点击“选择BIOS文件并提取”按钮，在弹出的文件选择窗口中，找到并选中要修改的BIOS文件，点击“打开”。  
Click the "选择BIOS文件并提取 (Select BIOS File and Extract)" button. In the pop-up file selection window, locate and select the BIOS file to modify, then click "打开 (Open)".  

![选择BIOS文件](https://raw.githubusercontent.com/jhsvip/ue-assist/main/教程/2OpenBios.jpg)  


### 2.3 等待提取完成（Wait for Extraction）
程序开始提取BIOS模块，进度条显示提取进度。提取完成后会弹出成功提示，点击“确定”即可。  
The program starts extracting BIOS modules, with a progress bar showing progress. A success prompt will appear when complete; click "确定 (OK)".  

![提取成功提示](https://raw.githubusercontent.com/jhsvip/ue-assist/main/教程/3ExtractDone.jpg)  


### 2.4 查看提取结果（Check Extraction Results）
提取完成后，软件同目录下会生成`_Setup`文件夹，包含提取的所有模块文件。打开该文件夹确认文件齐全（如`SETUP.sct`、`SETUPDATA.bin`等）。  
After extraction, a `_Setup` folder will be generated in the software directory, containing all extracted module files. Open the folder to confirm all files are present (e.g., `SETUP.sct`, `SETUPDATA.bin`).  

![打开工作目录](https://raw.githubusercontent.com/jhsvip/ue-assist/main/教程/4OpenWorkFolder.jpg)  


## 三、修改BIOS模块（Modifying BIOS Modules）
### 3.1 确认提取文件（Confirm Extracted Files）
检查`_Setup`文件夹中的核心文件：`amitse.sct`、`original_BIOS.bin`、`SETUP.sct`、`setup_ifr.txt`、`SETUPDATA.bin`，确保这些文件存在且大小正常（非空文件）。  
Check core files in the `_Setup` folder: `amitse.sct`, `original_BIOS.bin`, `SETUP.sct`, `setup_ifr.txt`, `SETUPDATA.bin`. Ensure these files exist and have normal sizes (non-empty).  

![检查提取文件](https://raw.githubusercontent.com/jhsvip/ue-assist/main/教程/5CheckFiles.jpg)  


### 3.2 上传文件到UEFI Editor（Upload Files to UEFI Editor）
打开浏览器访问`https://boringboredom.github.io/UEFI-Editor/`，分别上传`_Setup`文件夹中的对应文件：  国内汉化后的网站：http://ue.5argb.com/
- 点击`Setup SCT`上传`SETUP.sct`  
- 点击`IFR Extractor output TXT`上传`setup_ifr.txt`  
- 点击`AMITSE SCT`上传`amitse.sct`  
- 点击`Setupdata BIN`上传`SETUPDATA.bin`  

Open a browser and go to `https://boringboredom.github.io/UEFI-Editor/`. Upload corresponding files from the `_Setup` folder:  
- Click `Setup SCT` to upload `SETUP.sct`  
- Click `IFR Extractor output TXT` to upload `setup_ifr.txt`  
- Click `AMITSE SCT` to upload `amitse.sct`  
- Click `Setupdata BIN` to upload `SETUPDATA.bin`  

![上传文件到编辑器](https://raw.githubusercontent.com/jhsvip/ue-assist/main/教程/6UploadFiles.jpg)  


### 3.3 修改并下载模块（Modify and Download Modules）
在UEFI Editor左侧菜单找到需要修改的选项（如BIOS设置中的性能、超频相关选项），调整参数后点击界面底部的下载按钮，获取修改后的模块文件。  
In the UEFI Editor, find options to modify in the left menu (e.g., performance or overclocking settings in BIOS). Adjust parameters and click the download button at the bottom to get modified module files.  

![修改并下载模块](https://raw.githubusercontent.com/jhsvip/ue-assist/main/教程/7EditAndDownload.jpg)  


### 3.4 重命名修改后的文件（Rename Modified Files）
将下载的修改文件保存到`_Setup`文件夹，并按规则重命名：在原文件名后添加`mod`后缀（如`SETUPmod.sct`、`SETUPDATAmod.bin`），确保文件名符合合并工具的识别规则。  
Save the downloaded modified files to the `_Setup` folder and rename them: add the `mod` suffix to the original filename (e.g., `SETUPmod.sct`, `SETUPDATAmod.bin`). Ensure filenames match the merge tool's recognition rules.  

![重命名修改文件](https://raw.githubusercontent.com/jhsvip/ue-assist/main/教程/8EidtFileName.jpg)  


## 四、合并修改后的模块（Merging Modified Modules）
### 4.1 执行合并操作（Perform Merge）
返回`UEFI-Edior辅助工具`，点击“执行合并操作”按钮。程序会自动识别`_Setup`文件夹中带`mod`后缀的文件，并将修改内容合并到原始BIOS中。  
Return to the `UEFI-Edior Assistant Tool` and click "执行合并操作 (Perform Merge Operation)". The program will automatically identify files with the `mod` suffix in the `_Setup` folder and merge modifications into the original BIOS.  


### 4.2 查看合并结果（Check Merge Result）
合并完成后，工具会弹出提示框显示合并成功，并告知修改后的BIOS文件保存路径（默认位于`_Setup`文件夹，如`BIOS_modified_both.bin`）。至此，整个BIOS修改流程完成。  
After merging, the tool will pop up a prompt indicating success and show the save path of the modified BIOS file (by default in the `_Setup` folder, e.g., `BIOS_modified_both.bin`). The entire BIOS modification process is now complete.  

![合并完成提示](https://raw.githubusercontent.com/jhsvip/ue-assist/main/教程/9Merg.jpg)  

