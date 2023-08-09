import tkinter as tk
from tkinter import messagebox
import psutil
import GPUtil
import platform

class SystemCheckerAppX86:
    def __init__(self, root):
        self.root = root
        self.root.title("YellOS System Checker - x86 Edition")

        self.label = tk.Label(root, text="YellOS System Checker - x86 Edition", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.check_button = tk.Button(root, text="Run System Check", command=self.run_system_check)
        self.check_button.pack()

    def run_system_check(self):
        total_ram_mb = psutil.virtual_memory().total / (1024 ** 2)
        ram_score = get_ram_score(total_ram_mb)
        cpu_score = get_cpu_score()
        total_vram_mb = check_vram()

        nvme_ssd_detected = check_nvme_ssd()

        storage_result = ""
        if nvme_ssd_detected:
            storage_result = "NVMe SSD detected"
        else:
            ssd_present = check_storage()
            storage_result = "Non-NVMe SSD detected" if ssd_present else "No SSD found"

        gpu_result = check_gpu()

        result_message = f"RAM Score: {ram_score}\nCPU Score: {cpu_score}\n"
        result_message += f"Total RAM: {total_ram_mb:.2f} MB\n{storage_result}\n"
        result_message += f"GPU: {gpu_result}"

        messagebox.showinfo("System Check Results", result_message)

def get_ram_score(total_ram_mb):
    if total_ram_mb >= 512:
        return "Meets Standard RAM Requirements"
    elif total_ram_mb >= 128:
        return "Meets Core RAM Requirements"
    else:
        return "Doesn't Meet RAM Requirements"

def get_cpu_score():
    cpu_freq_mhz = psutil.cpu_freq().current
    if cpu_freq_mhz >= 850:
        return "Meets Standard CPU Requirements"
    elif cpu_freq_mhz >= 700:
        return "Meets Core CPU Requirements"
    else:
        return "Doesn't Meet CPU Requirements"

def check_vram():
    # Implement VRAM check logic here
    pass

def check_nvme_ssd():
    nvme_ssd_present = False
    for drive in psutil.disk_partitions():
        if "nvme" in drive.device.lower():
            nvme_ssd_present = True
            break

    return nvme_ssd_present
def check_storage():
    nvme_ssd_detected = check_nvme_ssd()

    if nvme_ssd_detected:
        print("NVMe SSD detected")
    else:
        ssd_present = False
        for drive in psutil.disk_partitions():
            if "ssd" in drive.opts.lower() or "ssd" in drive.fstype.lower():
                ssd_present = True
                break

        if ssd_present:
            print("Non-NVMe SSD detected")
        else:
            print("No SSD found")

    total_storage_gb = psutil.disk_usage("/").free / (1024 ** 3)
    print(f"Total Free Storage: {total_storage_gb:.2f} GB")

    if total_storage_gb >= 15:
        print("YellOS Carrot is ready for installation!")
    else:
        print("Insufficient free space for YellOS Carrot installation.")

def check_gpu():
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu_model = gpus[0].name  # Assuming you want the first GPU's model
            total_vram_mb = gpus[0].memoryTotal
            gpu_result = f"GPU Model: {gpu_model}\nTotal VRAM: {total_vram_mb} MB"
        else:
            gpu_result = "No GPU detected"
    except Exception as e:
        gpu_result = f"Error retrieving GPU info: {str(e)}"

    return gpu_result

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemCheckerAppX86(root)
    root.mainloop()
