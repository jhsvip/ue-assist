import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
import shutil
from threading import Thread
import time
import sys
import ctypes

def is_admin():
    """检查程序是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """重新以管理员权限启动程序"""
    if is_admin():
        return True
    else:
        print("正在请求管理员权限...")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        return False

if __name__ == "__main__":
    if not run_as_admin():
        sys.exit(0)
    
    print("已获取管理员权限，开始执行程序...")

class UEFIEditorAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("UEFI-Edior辅助工具 1.2  及叔出品")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f0f0")
        
        self.root.option_add("*Font", "SimHei 10")
        
        # 工具路径
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.UEFIEXTRACT = os.path.join(self.script_dir, "UEFIExtract.exe")
        self.IFR_EXTRACTOR = os.path.join(self.script_dir, "ifrextractor.exe")
        self.UEFIREPLACE = os.path.join(self.script_dir, "UEFIReplace.exe")
        
        # 状态标记
        self.setupdata_decompressed = False
        self.decompress_finished = False
        self.amitse_extracted = False
        
        # 语言设置
        self.language = "zh"
        self.translations = self.load_translations()
        
        self.create_styles()
        self.create_widgets()
        
        self.total_steps = 0
        self.current_step = 0

    def load_translations(self):
        """加载翻译字典"""
        return {
            "zh": {
                "title": "UEFI-Edior辅助工具",
                "description": "提取BIOS文件并合并修改后的模块（支持自动识别可合并文件）",
                "extract_button": "选择BIOS文件并提取",
                "merge_button": "执行合并操作",
                "progress_label": "进度:",
                "status_label": "执行日志（详细）:",
                "extract_info": "提取功能说明:\n"
                                "1. 点击'选择BIOS文件并提取'按钮\n"
                                "2. 选择需要提取的BIOS文件\n"
                                "3. 程序会将文件提取到_Setup文件夹",
                "merge_info": "合并功能说明:\n"
                              "1. 修改提取的模块并按规则保存：\n"
                              "   - SETUP模块 → SETUPmod.sct\n"
                              "   - SETUPDATA模块 → SETUPDATAmod.bin\n"
                              "2. 程序会自动识别可合并的文件（支持单独/同时合并）\n"
                              "3. 点击'执行合并操作'按钮即可完成合并",
                "language": "语言",
                "chinese": "中文",
                "english": "英文",
                "extracting": "正在提取模块【{0}】（GUID: {1}）",
                "trying_type": "将尝试的模块类型: {0}",
                "extraction_success": "【{0}】提取成功",
                "extraction_failure": "【{0}】所有类型尝试失败（GUID: {1}）",
                "decompressing": "开始检查SETUPDATA.bin是否需要解压...",
                "decompression_success": "SETUPDATA解压成功，找到{0}个文件",
                "performing_ifr": "执行IFR分析（文件: {0}）",
                "ifr_success": "IFR分析完成",
                "results_summary": "\n===== 提取结果汇总 =====",
                "original_bios": "原始BIOS文件",
                "setup_module": "SETUP模块",
                "setupdata_module": "SETUPDATA模块",
                "decompressed_setupdata": "解压后的SETUPDATA",
                "amitse_module": "AMITSE模块",
                "ifr_analysis": "IFR分析结果",
                "success": "成功",
                "failure": "失败",
                "failure_no_module": "失败（可能BIOS中无此模块）",
                "all_success": "所有模块提取成功！",
                "partial_failure": "部分模块提取失败（非必须模块可能不影响使用）",
                "merging": "开始合并操作...",
                "merging_setup": "正在合并SETUP模块...",
                "merging_setupdata": "正在合并SETUPDATA模块...",
                "merge_success": "合并成功！输出文件: {0}",
                "merge_failure": "合并失败（未生成输出文件）",
                "merge_complete_setup": "SETUP模块合并完成！修改后的BIOS已保存到:\n{0}",
                "merge_complete_setupdata": "SETUPDATA模块合并完成！修改后的BIOS已保存到:\n{0}",
                "merge_complete_both": "两种模块合并完成！修改后的BIOS已保存到:\n{0}",
                "no_merge_files": "未检测到任何可合并文件（需要SETUPmod.sct或SETUPDATAmod.bin）",
                "setup_mod_missing": "未找到SETUPmod.sct，跳过SETUP模块合并",
                "setupdata_mod_missing": "未找到SETUPDATAmod.bin，跳过SETUPDATA模块合并"
            },
            "en": {
                "title": "UEFI-Editor Assistant",
                "description": "Extract BIOS files and merge modified modules (auto-detect mergeable files)",
                "extract_button": "Select BIOS File and Extract",
                "merge_button": "Perform Merge Operation",
                "progress_label": "Progress:",
                "status_label": "Execution Log (Detailed):",
                "extract_info": "Extraction Instructions:\n"
                                "1. Click 'Select BIOS File and Extract'\n"
                                "2. Select the BIOS file to extract\n"
                                "3. Files will be extracted to _Setup folder",
                "merge_info": "Merge Instructions:\n"
                              "1. Modify extracted modules and save as:\n"
                              "   - SETUP module → SETUPmod.sct\n"
                              "   - SETUPDATA module → SETUPDATAmod.bin\n"
                              "2. The program automatically identifies mergeable files\n"
                              "3. Click 'Perform Merge Operation' to complete merging",
                "language": "Language",
                "chinese": "Chinese",
                "english": "English",
                "extracting": "Extracting module 【{0}】 (GUID: {1})",
                "trying_type": "Module types to try: {0}",
                "extraction_success": "【{0}】Extraction successful",
                "extraction_failure": "【{0}】All types failed (GUID: {1})",
                "decompressing": "Checking if SETUPDATA.bin needs decompression...",
                "decompression_success": "SETUPDATA decompressed successfully, found {0} files",
                "performing_ifr": "Performing IFR analysis (File: {0})",
                "ifr_success": "IFR analysis completed",
                "results_summary": "\n===== Extraction Results Summary =====",
                "original_bios": "Original BIOS File",
                "setup_module": "SETUP Module",
                "setupdata_module": "SETUPDATA Module",
                "decompressed_setupdata": "Decompressed SETUPDATA",
                "amitse_module": "AMITSE Module",
                "ifr_analysis": "IFR Analysis Result",
                "success": "Success",
                "failure": "Failure",
                "failure_no_module": "Failure (Module may not exist in BIOS)",
                "all_success": "All modules extracted successfully!",
                "partial_failure": "Some modules failed to extract (non-essential modules may not affect usage)",
                "merging": "Starting merge operation...",
                "merging_setup": "Merging SETUP module...",
                "merging_setupdata": "Merging SETUPDATA module...",
                "merge_success": "Merge successful! Output file: {0}",
                "merge_failure": "Merge failed (output file not generated)",
                "merge_complete_setup": "SETUP module merge completed! Modified BIOS saved to:\n{0}",
                "merge_complete_setupdata": "SETUPDATA module merge completed! Modified BIOS saved to:\n{0}",
                "merge_complete_both": "Both modules merged! Modified BIOS saved to:\n{0}",
                "no_merge_files": "No mergeable files detected (requires SETUPmod.sct or SETUPDATAmod.bin)",
                "setup_mod_missing": "SETUPmod.sct not found, skipping SETUP module merge",
                "setupdata_mod_missing": "SETUPDATAmod.bin not found, skipping SETUPDATA module merge"
            }
        }

    def create_styles(self):
        """创建自定义样式"""
        style = ttk.Style()
        
        style.configure("Title.TLabel", 
                        background="#4a7abc", 
                        foreground="white",
                        font=("SimHei", 18, "bold"),
                        anchor="center")
        
        style.configure("Extraction.TButton",
                       font=("SimHei", 12),
                       foreground="white",
                       background="#4CAF50",
                       padding=10)
        
        style.configure("Merge.TButton",
                       font=("SimHei", 12),
                       foreground="white",
                       background="#2196F3",
                       padding=10)
        
        style.map("Extraction.TButton",
                 background=[('active', '#45a049'), ('pressed', '#3d8b40')])
        style.map("Merge.TButton",
                 background=[('active', '#0b7dda'), ('pressed', '#0066cc')])
        
        style.configure("Custom.Horizontal.TProgressbar",
                       background="#4CAF50",
                       troughcolor="#d9d9d9",
                       bordercolor="#d9d9d9",
                       lightcolor="#4CAF50",
                       darkcolor="#4CAF50")
        
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0")

    def create_widgets(self):
        # 顶部标题
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.title_label = tk.Label(title_frame, 
                              text=self.translations[self.language]["title"], 
                              font=("SimHei", 18, "bold"),
                              bg="#4a7abc",
                              fg="white",
                              anchor="center")
        self.title_label.pack(fill=tk.X)
        
        # 语言选择
        lang_frame = ttk.Frame(self.root)
        lang_frame.pack(fill=tk.X, padx=10, pady=5)
        
        lang_label = ttk.Label(lang_frame, text=self.translations[self.language]["language"] + ":")
        lang_label.pack(side=tk.LEFT, padx=5)
        
        self.lang_var = tk.StringVar(value=self.language)
        lang_combobox = ttk.Combobox(lang_frame, textvariable=self.lang_var, values=["zh", "en"], state="readonly", width=5)
        lang_combobox.pack(side=tk.LEFT, padx=5)
        lang_combobox.bind("<<ComboboxSelected>>", self.change_language)
        
        # 说明文本
        desc_frame = ttk.Frame(self.root)
        desc_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.desc_label = ttk.Label(desc_frame, 
                             text=self.translations[self.language]["description"], 
                             font=("SimHei", 11))
        self.desc_label.pack()
        
        # 按钮区域（移除了检测提示区域）
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=10, pady=20)
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)
        
        # 左侧按钮（提取）
        left_btn_frame = ttk.Frame(btn_frame)
        left_btn_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5))
        
        self.btn_extract = tk.Button(left_btn_frame, 
                                    text=self.translations[self.language]["extract_button"], 
                                    command=self.select_bios_file,
                                    font=("SimHei", 12),
                                    bg="#4CAF50",
                                    fg="white",
                                    relief=tk.RAISED,
                                    bd=2)
        self.btn_extract.pack(pady=5, fill=tk.X)
        
        # 右侧按钮（合并）- 直接显示按钮，无检测提示
        right_btn_frame = ttk.Frame(btn_frame)
        right_btn_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10))
        
        self.btn_merge = tk.Button(right_btn_frame, 
                                  text=self.translations[self.language]["merge_button"], 
                                  command=self.run_replace_script,
                                  font=("SimHei", 12),
                                  bg="#2196F3",
                                  fg="white",
                                  relief=tk.RAISED,
                                  bd=2)
        self.btn_merge.pack(pady=5, fill=tk.X)
        
        # 进度条
        progress_frame = ttk.Frame(self.root)
        progress_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.progress_label = ttk.Label(progress_frame, 
                                 text=self.translations[self.language]["progress_label"])
        self.progress_label.pack(anchor=tk.W)
        
        # 进度条容器
        progress_bar_frame = ttk.Frame(progress_frame)
        progress_bar_frame.pack(fill=tk.X, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_bar_frame, 
                                           variable=self.progress_var, 
                                           length=660, mode='determinate',
                                           style="Custom.Horizontal.TProgressbar")
        self.progress_bar.pack(fill=tk.X, padx=2, pady=2)
        
        self.progress_percent = tk.Label(progress_bar_frame, 
                                        text="0%", 
                                        font=("SimHei", 10, "bold"), 
                                        bg="#4CAF50", 
                                        fg="white",
                                        padx=5, pady=1)
        self.progress_percent.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # 分割窗格
        paned_window = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 状态文本框
        status_frame = ttk.Frame(paned_window)
        paned_window.add(status_frame, weight=4)
        
        self.status_label = ttk.Label(status_frame, 
                               text=self.translations[self.language]["status_label"])
        self.status_label.pack(anchor=tk.W)
        
        self.status_text = tk.Text(status_frame, wrap=tk.WORD,
                                  bg="white", fg="#333333",
                                  font=("SimHei", 10),
                                  highlightthickness=1)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(self.status_text, command=self.status_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar.config(bg="#f0f0f0", relief=tk.FLAT)
        self.status_text.config(yscrollcommand=scrollbar.set)
        
        # 说明文本区域
        info_frame = ttk.Frame(paned_window)
        paned_window.add(info_frame, weight=1)
        
        self.extract_info = ttk.Label(info_frame, 
                              text=self.translations[self.language]["extract_info"],
                              justify=tk.LEFT, wraplength=680)
        self.extract_info.pack(anchor=tk.NW, padx=10, pady=5)
        
        self.merge_info = ttk.Label(info_frame, 
                           text=self.translations[self.language]["merge_info"],
                           justify=tk.LEFT, wraplength=680)
        self.merge_info.pack(anchor=tk.NW, padx=10, pady=5)

    def change_language(self, event=None):
        """更改语言"""
        self.language = self.lang_var.get()
        
        # 更新界面文本
        self.root.title(self.translations[self.language]["title"])
        self.title_label.config(text=self.translations[self.language]["title"])
        self.desc_label.config(text=self.translations[self.language]["description"])
        self.btn_extract.config(text=self.translations[self.language]["extract_button"])
        self.btn_merge.config(text=self.translations[self.language]["merge_button"])
        self.progress_label.config(text=self.translations[self.language]["progress_label"])
        self.status_label.config(text=self.translations[self.language]["status_label"])
        self.extract_info.config(text=self.translations[self.language]["extract_info"])
        self.merge_info.config(text=self.translations[self.language]["merge_info"])
        
        # 清空日志
        self.status_text.delete(1.0, tk.END)

    def update_status(self, message, *args):
        """更新日志显示"""
        if args:
            message = message.format(*args)
            
        timestamp = time.strftime("[%H:%M:%S] ")
        self.status_text.insert(tk.END, timestamp + message + "\n")
        self.status_text.see(tk.END)
        
    def update_progress(self):
        """更新进度条"""
        self.current_step += 1
        if self.total_steps > 0:
            progress = (self.current_step / self.total_steps) * 100
            self.progress_var.set(progress)
            self.progress_percent.config(text=f"{int(progress)}%")
        self.root.update_idletasks()
        
    def force_progress_complete(self):
        """强制进度条到100%"""
        self.progress_var.set(100)
        self.progress_percent.config(text="100%")
        self.root.update_idletasks()

    def extract_module(self, guid, target_dir, types, output_file_name):
        """提取指定模块"""
        self.update_status(self.translations[self.language]["extracting"], output_file_name, guid)
        self.update_status(self.translations[self.language]["trying_type"], types)
        
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir, ignore_errors=True)
        
        for t in types:
            try:
                tool_abs_path = os.path.abspath(self.UEFIEXTRACT)
                bios_abs_path = os.path.abspath(self.bios_file)
                target_abs_dir = os.path.abspath(target_dir)
                
                command = f'"{tool_abs_path}" "{bios_abs_path}" "{guid}" -o "{target_abs_dir}" -m body -t {t}'
                self.update_status(f"尝试类型【{t}】的命令: {command}")
                
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    self.update_status(f"类型【{t}】命令执行成功（返回码: 0）")
                else:
                    self.update_status(f"类型【{t}】命令执行失败（返回码: {result.returncode}）")
                    self.update_status(f"错误输出: {result.stderr[:300]}")
                
                body_bin_path = os.path.join(target_abs_dir, "body.bin")
                if os.path.exists(body_bin_path) and os.path.getsize(body_bin_path) > 0:
                    self.update_status(f"找到提取文件: {body_bin_path}（大小: {os.path.getsize(body_bin_path)}字节）")
                    
                    output_abs_file = os.path.abspath(os.path.join("_Setup", output_file_name))
                    try:
                        shutil.move(body_bin_path, output_abs_file)
                        self.update_status(f"已将文件移动到: {output_abs_file}")
                        shutil.rmtree(target_abs_dir, ignore_errors=True)
                        self.update_status(self.translations[self.language]["extraction_success"], output_file_name)
                        return True
                    except Exception as e:
                        self.update_status(f"移动文件失败: {str(e)}（但提取已成功）")
                        return True
                else:
                    self.update_status(f"类型【{t}】未提取到有效文件（{body_bin_path}不存在或为空）")
            
            except subprocess.TimeoutExpired:
                self.update_status(f"类型【{t}】命令超时（30秒）")
            except Exception as e:
                self.update_status(f"类型【{t}】执行出错: {str(e)}")
        
        self.update_status(self.translations[self.language]["extraction_failure"], output_file_name, guid)
        return False
        
    def decompress_setupdata(self):
        """解压SETUPDATA.bin"""
        self.setupdata_decompressed = False
        self.decompress_finished = False
        
        setupdata_bin = os.path.join("_Setup", "SETUPDATA.bin")
        setupdata_abs = os.path.abspath(setupdata_bin)
        
        if not os.path.exists(setupdata_abs):
            self.update_status(f"未找到SETUPDATA.bin（路径: {setupdata_abs}），跳过解压")
            self.decompress_finished = True
            return False
            
        if not os.access(setupdata_abs, os.R_OK):
            self.update_status(f"无读取权限: {setupdata_abs}（请以管理员身份运行）")
            self.decompress_finished = True
            return False
            
        self.update_status(self.translations[self.language]["decompressing"])
        
        # 判断是否需要解压
        try:
            if os.path.getsize(setupdata_abs) < 1024 * 1024:  # 1MB阈值
                self.update_status("SETUPDATA.bin无需解压（文件大小较小，视为未压缩状态）")
                self.setupdata_decompressed = True
                self.decompress_finished = True
                return True
        except Exception as e:
            self.update_status(f"判断文件是否需要解压时出错: {str(e)}")
        
        # 创建解压目录
        unpack_dir = os.path.abspath("_Setup\\SETUPDATA_unpacked")
        try:
            if os.path.exists(unpack_dir):
                shutil.rmtree(unpack_dir, ignore_errors=True)
            os.makedirs(unpack_dir, exist_ok=True)
            self.update_status(f"解压目标目录: {unpack_dir}")
        except Exception as e:
            self.update_status(f"创建解压目录失败: {str(e)}")
            self.decompress_finished = True
            return False
        
        # 执行解压命令
        try:
            tool_abs_path = os.path.abspath(self.UEFIEXTRACT)
            command = f'"{tool_abs_path}" "{setupdata_abs}" -d -o "{unpack_dir}"'
            self.update_status(f"执行解压命令: {command}")
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            self.update_status(f"解压命令返回码: {result.returncode}（0表示成功）")
            
            # 检查解压结果
            unpack_files = []
            for root_dir, subdirs, files in os.walk(unpack_dir):
                unpack_files.extend([os.path.join(root_dir, f) for f in files])
            
            if len(unpack_files) > 0:
                self.update_status(self.translations[self.language]["decompression_success"], len(unpack_files))
                self.setupdata_decompressed = True
            else:
                self.update_status("解压后未找到有效文件，删除空目录")
                shutil.rmtree(unpack_dir, ignore_errors=True)
                if os.path.exists(setupdata_abs) and os.path.getsize(setupdata_abs) > 0:
                    self.update_status("使用原始SETUPDATA.bin（无需解压）")
                    self.setupdata_decompressed = True
    
        except subprocess.TimeoutExpired:
            self.update_status("解压命令超时（60秒）")
            if os.path.exists(unpack_dir):
                shutil.rmtree(unpack_dir, ignore_errors=True)
        except Exception as e:
            self.update_status(f"解压命令执行失败: {str(e)}")
            if os.path.exists(unpack_dir):
                shutil.rmtree(unpack_dir, ignore_errors=True)
        finally:
            if os.path.exists(unpack_dir):
                try:
                    if not os.listdir(unpack_dir):
                        shutil.rmtree(unpack_dir, ignore_errors=True)
                        self.update_status("删除空解压目录")
                except Exception as e:
                    self.update_status(f"删除空目录失败: {str(e)}")
    
        self.decompress_finished = True
        return self.setupdata_decompressed

    def perform_ifr_analysis(self):
        """执行IFR分析"""
        setup_sct = os.path.join("_Setup", "SETUP.sct")
        if not os.path.exists(setup_sct):
            self.update_status("未找到SETUP.sct，无法执行IFR分析")
            return False
            
        self.update_status(self.translations[self.language]["performing_ifr"], setup_sct)
        try:
            tool_abs_path = os.path.abspath(self.IFR_EXTRACTOR)
            command = f'"{tool_abs_path}" "{setup_sct}" verbose'
            subprocess.run(command, shell=True, timeout=30)
            
            ifr_file = os.path.join("_Setup", "SETUP.sct.0.0.en-US.ifr.txt")
            if os.path.exists(ifr_file):
                setup_ifr = os.path.join("_Setup", "setup_ifr.txt")
                shutil.move(ifr_file, setup_ifr)
                self.update_status(f"IFR文件已保存到: {setup_ifr}")
                self.update_status(self.translations[self.language]["ifr_success"])
                return True
            else:
                self.update_status("未生成IFR文件（分析失败）")
                return False
        except Exception as e:
            self.update_status(f"IFR分析出错: {str(e)}")
            return False
        
    def print_extraction_results(self):
        """显示提取结果"""
        # 等待解压完成
        wait_seconds = 0
        while not self.decompress_finished and wait_seconds < 15:
            self.update_status(f"等待SETUPDATA解压完成（已等{wait_seconds}秒）...")
            time.sleep(1)
            wait_seconds += 1
    
        self.update_status(self.translations[self.language]["results_summary"])
    
        # 检查各文件状态
        def check_status(file_path, name_key, use_decompress=False, use_amitse=False):
            if use_decompress:
                status = self.translations[self.language]["success"] if self.setupdata_decompressed else self.translations[self.language]["failure"]
            elif use_amitse:
                status = self.translations[self.language]["success"] if self.amitse_extracted else self.translations[self.language]["failure_no_module"]
            else:
                if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                    status = self.translations[self.language]["success"]
                else:
                    status = self.translations[self.language]["failure"]
        
            name = self.translations[self.language][name_key]
            self.update_status(f"[{'✓' if status == self.translations[self.language]['success'] else '✗'}] {name}: {status}")
            return status == self.translations[self.language]["success"]
    
        # 定义检测项
        results = [
            (os.path.join("_Setup", "original_BIOS.bin"), "original_bios", False, False),
            (os.path.join("_Setup", "SETUP.sct"), "setup_module", False, False),
            (os.path.join("_Setup", "SETUPDATA.bin"), "setupdata_module", False, False),
            ("", "decompressed_setupdata", True, False),
            (os.path.join("_Setup", "amitse.sct"), "amitse_module", False, True),
            (os.path.join("_Setup", "setup_ifr.txt"), "ifr_analysis", False, False)
        ]
    
        all_success = True
        for path, name_key, use_decompress, use_amitse in results:
            if not check_status(path, name_key, use_decompress, use_amitse):
                all_success = False
            
        self.update_status("=======================")
        self.update_status("提示：若AMITSE模块失败，可能是BIOS中没有该模块（非必须文件）")
    
        if all_success:
            messagebox.showinfo("完成", self.translations[self.language]["all_success"])
        else:
            messagebox.showwarning("注意", self.translations[self.language]["partial_failure"])
        
        self.force_progress_complete()
        
    def select_bios_file(self):
        """选择BIOS文件"""
        self.bios_file = filedialog.askopenfilename(
            title="选择BIOS文件",
            filetypes=[("所有文件", "*.*")]
        )
        if not self.bios_file:
            return
            
        # 重置状态
        self.total_steps = 7
        self.current_step = 0
        self.progress_var.set(0)
        self.status_text.delete(1.0, tk.END)
        self.setupdata_decompressed = False
        self.decompress_finished = False
        self.amitse_extracted = False
        
        # 禁用按钮
        self.btn_extract.config(state=tk.DISABLED)
        self.btn_merge.config(state=tk.DISABLED)
        
        # 启动提取线程
        Thread(target=self.run_extract_script, daemon=True).start()
        
    def run_extract_script(self):
        """执行提取逻辑"""
        try:
            self.update_status(f"选择的BIOS文件: {self.bios_file}（大小: {os.path.getsize(self.bios_file)}字节）")
            
            # 步骤1：检查BIOS文件
            if not os.path.exists(self.bios_file):
                self.update_status("错误：BIOS文件不存在")
                messagebox.showerror("错误", "BIOS文件不存在")
                return
            self.update_progress()
            
            # 步骤2：检查工具是否齐全
            tools = [
                (self.UEFIEXTRACT, "UEFIExtract.exe（提取模块用）"),
                (self.IFR_EXTRACTOR, "ifrextractor.exe（IFR分析用）"),
                (self.UEFIREPLACE, "UEFIReplace.exe（合并用）")
            ]
            missing = []
            for path, desc in tools:
                if not os.path.exists(path):
                    missing.append(f"{desc}（路径: {path}）")
            if missing:
                self.update_status("错误：缺少必要工具：")
                for m in missing:
                    self.update_status(f"- {m}")
                messagebox.showerror("错误", f"缺少工具：\n{', '.join([m.split('（')[0] for m in missing])}")
                return
            self.update_progress()
            
            # 步骤3：创建_Setup目录
            setup_dir = "_Setup"
            if os.path.exists(setup_dir):
                self.update_status(f"清理旧目录: {setup_dir}")
                shutil.rmtree(setup_dir, ignore_errors=True)
            os.makedirs(setup_dir, exist_ok=True)
            self.update_status(f"创建目录: {os.path.abspath(setup_dir)}")
            self.update_progress()
            
            # 步骤4：复制原始BIOS
            original_bios = os.path.join(setup_dir, "original_BIOS.bin")
            try:
                shutil.copy2(self.bios_file, original_bios)
                self.update_status(f"复制原始BIOS到: {original_bios}")
            except Exception as e:
                self.update_status(f"复制BIOS失败: {str(e)}")
                messagebox.showerror("错误", "复制原始BIOS失败")
                return
            self.update_progress()
            
            # 步骤5：提取模块
            self.update_status("\n===== 开始提取模块 =====")
            
            # 提取SETUP模块
            setup_success = self.extract_module(
                "899407D7-99FE-43D8-9A21-79EC328CAC21",
                "_Setup\\temp_setup",
                [10, 18, 22],
                "SETUP.sct"
            )
            
            # 提取SETUPDATA模块
            setupdata_success = self.extract_module(
                "FE612B72-203C-47B1-8560-A66D946EB371",
                "_Setup\\temp_setupdata",
                [10, 18, 22],
                "SETUPDATA.bin"
            )
            
            # 步骤6：解压SETUPDATA + 提取AMITSE
            if setupdata_success:
                self.decompress_setupdata()
            else:
                self.update_status("SETUPDATA提取失败，跳过解压")
                self.decompress_finished = True
            
            # 提取AMITSE模块
            self.amitse_extracted = self.extract_module(
                "B1DA0ADF-4F77-4070-A88E-BFFE1C60529A",
                "_Setup\\temp_amitse",
                [10, 18, 22, 30],
                "amitse.sct"
            )
            self.update_progress()
            
            # 步骤7：IFR分析
            self.update_status("\n===== 开始IFR分析 =====\n")
            if setup_success:
                self.perform_ifr_analysis()
            else:
                self.update_status("SETUP模块提取失败，跳过IFR分析")
            self.update_progress()
            
            # 显示结果
            self.print_extraction_results()
            
        except Exception as e:
            self.update_status(f"提取过程出错: {str(e)}")
            messagebox.showerror("错误", f"提取出错: {str(e)}")
        finally:
            # 恢复按钮
            self.btn_extract.config(state=tk.NORMAL)
            self.btn_merge.config(state=tk.NORMAL)
    
    # 合并SETUP模块的方法
    def merge_setup_module(self, bios_file, output_file):
        """合并SETUP模块（SETUPmod.sct）"""
        MODIFIED_FILE = os.path.abspath("_Setup\\SETUPmod.sct")
        MODULE_GUID = "899407D7-99FE-43D8-9A21-79EC328CAC21"  # SETUP模块GUID
        SECTION_TYPE = "18"  # SETUP模块类型
        
        # 检查修改文件是否存在
        if not os.path.exists(MODIFIED_FILE) or os.path.getsize(MODIFIED_FILE) == 0:
            self.update_status(self.translations[self.language]["setup_mod_missing"])
            return False, None
            
        # 执行合并
        try:
            self.update_status(self.translations[self.language]["merging_setup"])
            command = f'"{self.UEFIREPLACE}" "{bios_file}" "{MODULE_GUID}" "{SECTION_TYPE}" "{MODIFIED_FILE}" -o "{output_file}"'
            self.update_status(f"执行SETUP合并命令: {command}")
            
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            # 检查合并结果
            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                self.update_status(self.translations[self.language]["merge_success"], output_file)
                return True, output_file
            else:
                self.update_status(self.translations[self.language]["merge_failure"])
                self.update_status(f"命令输出: {result.stdout}")
                self.update_status(f"命令错误: {result.stderr}")
                return False, None
        except Exception as e:
            self.update_status(f"SETUP模块合并出错: {str(e)}")
            return False, None
    
    # 合并SETUPDATA模块的方法
    def merge_setupdata_module(self, bios_file, output_file):
        """合并SETUPDATA模块（SETUPDATAmod.bin）"""
        MODIFIED_FILE = os.path.abspath("_Setup\\SETUPDATAmod.bin")
        MODULE_GUID = "FE612B72-203C-47B1-8560-A66D946EB371"  # SETUPDATA模块GUID
        SECTION_TYPE = "18"  # SETUPDATA模块类型
        
        # 检查修改文件是否存在
        if not os.path.exists(MODIFIED_FILE) or os.path.getsize(MODIFIED_FILE) == 0:
            self.update_status(self.translations[self.language]["setupdata_mod_missing"])
            return False, None
            
        # 执行合并
        try:
            self.update_status(self.translations[self.language]["merging_setupdata"])
            command = f'"{self.UEFIREPLACE}" "{bios_file}" "{MODULE_GUID}" "{SECTION_TYPE}" "{MODIFIED_FILE}" -o "{output_file}"'
            self.update_status(f"执行SETUPDATA合并命令: {command}")
            
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            # 检查合并结果
            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                self.update_status(self.translations[self.language]["merge_success"], output_file)
                return True, output_file
            else:
                self.update_status(self.translations[self.language]["merge_failure"])
                self.update_status(f"命令输出: {result.stdout}")
                self.update_status(f"命令错误: {result.stderr}")
                return False, None
        except Exception as e:
            self.update_status(f"SETUPDATA模块合并出错: {str(e)}")
            return False, None
            
    def run_replace_script(self):
        """执行合并逻辑"""
        self.status_text.delete(1.0, tk.END)
        self.btn_extract.config(state=tk.DISABLED)
        self.btn_merge.config(state=tk.DISABLED)
        
        Thread(target=self._run_replace_script, daemon=True).start()
        
    def _run_replace_script(self):
        """合并核心逻辑（自动检测可合并文件）"""
        try:
            # 基础路径
            BIOS_FILE = os.path.abspath("_Setup\\original_BIOS.bin")
            BASE_OUTPUT = os.path.abspath("_Setup\\BIOS_modified")
            
            # 检测可合并文件（实际存在性）
            setup_mod_exists = os.path.exists(os.path.abspath("_Setup\\SETUPmod.sct")) and os.path.getsize(os.path.abspath("_Setup\\SETUPmod.sct")) > 0
            setupdata_mod_exists = os.path.exists(os.path.abspath("_Setup\\SETUPDATAmod.bin")) and os.path.getsize(os.path.abspath("_Setup\\SETUPDATAmod.bin")) > 0
            
            # 检查是否有可合并文件
            if not setup_mod_exists and not setupdata_mod_exists:
                self.update_status(self.translations[self.language]["no_merge_files"])
                messagebox.showerror("错误", self.translations[self.language]["no_merge_files"])
                return
                
            # 根据实际可合并文件数量设置步骤数
            merge_count = 0
            if setup_mod_exists:
                merge_count += 1
            if setupdata_mod_exists:
                merge_count += 1
            self.total_steps = merge_count + 1  # 检查步骤 + 合并步骤数
            
            self.update_status(self.translations[self.language]["merging"])
            
            # 检查基础文件
            missing = []
            if not os.path.exists(BIOS_FILE):
                missing.append(f"原始BIOS文件（{BIOS_FILE}）")
            if not os.path.exists(self.UEFIREPLACE):
                missing.append(f"UEFIReplace.exe（{self.UEFIREPLACE}）")
                
            if missing:
                self.update_status("缺少合并所需文件：")
                for m in missing:
                    self.update_status(f"- {m}")
                messagebox.showerror("错误", f"缺少文件：\n{', '.join(missing)}")
                return
                
            self.update_progress()
            
            # 执行合并（根据实际存在的文件）
            current_bios = BIOS_FILE  # 当前使用的BIOS文件
            final_output = ""
            
            # 合并SETUP模块（如果存在）
            if setup_mod_exists:
                temp_output = f"{BASE_OUTPUT}_setup_temp.bin"
                success, output = self.merge_setup_module(current_bios, temp_output)
                if success and output:
                    current_bios = output  # 更新当前BIOS文件
                    final_output = output
                self.update_progress()
            
            # 合并SETUPDATA模块（如果存在）
            if setupdata_mod_exists:
                # 根据是否已合并SETUP模块确定输出文件名
                if setup_mod_exists:
                    output_file = f"{BASE_OUTPUT}_both.bin"
                else:
                    output_file = f"{BASE_OUTPUT}_setupdata.bin"
                    
                success, output = self.merge_setupdata_module(current_bios, output_file)
                if success and output:
                    final_output = output  # 更新最终输出
                self.update_progress()
            
            # 检查最终结果
            if os.path.exists(final_output) and os.path.getsize(final_output) > 0:
                # 根据合并类型显示对应信息
                if setup_mod_exists and setupdata_mod_exists:
                    msg = self.translations[self.language]["merge_complete_both"].format(final_output)
                elif setup_mod_exists:
                    msg = self.translations[self.language]["merge_complete_setup"].format(final_output)
                else:  # 仅setupdata
                    msg = self.translations[self.language]["merge_complete_setupdata"].format(final_output)
                    
                self.update_status(msg)
                messagebox.showinfo("成功", msg)
            else:
                self.update_status(self.translations[self.language]["merge_failure"])
                messagebox.showerror("错误", "合并失败")
                return
                
        except Exception as e:
            self.update_status(f"合并出错: {str(e)}")
            messagebox.showerror("错误", f"合并出错: {str(e)}")
        finally:
            self.btn_extract.config(state=tk.NORMAL)
            self.btn_merge.config(state=tk.NORMAL)
            self.force_progress_complete()

if __name__ == "__main__":
    root = tk.Tk()
    app = UEFIEditorAssistant(root)
    root.mainloop()
