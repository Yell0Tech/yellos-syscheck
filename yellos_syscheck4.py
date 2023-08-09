import tkinter as tk
from tkinter import messagebox
import psutil
import platform

class SystemCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YellOS System Checker")

        self.label = tk.Label(root, text="YellOS System Checker", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.check_button = tk.Button(root, text="Run System Check", command=self.run_system_check)
        self.check_button.pack()

    def run_system_check(self):
        total_ram_gb = psutil.virtual_memory().total / (1024 ** 3)
        ram_score = get_ram_score(total_ram_gb)
        ram_type = get_ram_type()
        ram_type_name = get_ram_type_name(ram_type)
        ram_type_score = get_ram_type_score(ram_type)

        nvme_ssd_detected = check_nvme_ssd()

        storage_result = ""
        if nvme_ssd_detected:
            storage_result = "NVMe SSD detected"
        else:
            ssd_present = check_storage()
            storage_result = "Non-NVMe SSD detected" if ssd_present else "No SSD found"

        cpu_result = check_cpu()

        gpu_result = check_gpu()

        result_message = f"RAM Score: {ram_score}\nRAM Type: {ram_type_name}\n"
        result_message += f"Total RAM: {total_ram_gb:.2f} GB\n{storage_result}\n"
        result_message += f"CPU: {cpu_result}\nGPU: {gpu_result}"

        messagebox.showinfo("System Check Results", result_message)

def get_ram_score(total_ram_gb):
    # Calculate RAM score based on total RAM
    if 1 <= total_ram_gb < 2:
        return "Ok"
    elif 2 <= total_ram_gb < 4:
        return "Yes"
    elif total_ram_gb >= 4:
        return "Perfect"
    else:
        return "Unknown"

def get_ram_type():
    # Determine RAM type based on system information
    system_info = platform.uname()
    # You can implement logic here to detect RAM type
    return "DDR4"

def get_ram_type_name(ram_type):
    # Map RAM type to human-readable name
    ram_type_names = {
        "DDR5": "DDR5",
        "DDR4": "DDR4",
        "DDR3": "DDR3",
        "DDR2": "DDR2",
        "DDR1": "DDR1",
        "Unknown": "Unknown",
    }
    return ram_type_names.get(ram_type, "Unknown")

def get_ram_type_score(ram_type):
    # Assign scores to RAM types
    scores = {
        "DDR5": 5,
        "DDR4": 4,
        "DDR3": 3,
        "DDR2": 2,
        "DDR1": 1,
        "Unknown": 0,
    }
    return scores.get(ram_type, 0)

def check_nvme_ssd():
    # Check if an NVMe SSD is present
    for drive in psutil.disk_partitions():
        if "nvme" in drive.device.lower():
            return True
    return False

def check_storage():
    # Check if SSD storage is present
    for drive in psutil.disk_partitions():
        if "ssd" in drive.opts.lower() or "ssd" in drive.fstype.lower():
            return True
    return False

def check_cpu():
    # Check CPU compatibility
    cpu_info = platform.uname()
    num_cores = psutil.cpu_count(logical=False)
    is_64bit = platform.machine().endswith('64')
    cpu_freq_ghz = psutil.cpu_freq().current / 1000

    cpu_result = "Compatible"
    if (not is_64bit) or (num_cores < 2) or (cpu_freq_ghz < 1):
        cpu_result = "Incompatible"

    return cpu_result

def check_gpu():
    # Check GPU compatibility
    gpu_info = psutil.virtual_memory()
    total_vram_mb = gpu_info.total / (1024 ** 2)

    gpu_result = "Compatible"
    if total_vram_mb < 128:
        gpu_result = "Incompatible"

    return gpu_result

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemCheckerApp(root)
    root.mainloop()
