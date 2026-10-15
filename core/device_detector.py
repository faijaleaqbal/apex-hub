import subprocess
import json

class DeviceDetector:
    @staticmethod
    def get_hardware_summary():
        summary = {
            "keyboard": {
                "name": "Karnage Visage Tri-Mode Gaming Keyboard",
                "model": "WLKM-054",
                "type": "Mecha-Membrane (84-Key TKL)",
                "connectivity": "2.4GHz Wireless / BT / Type-C",
                "knob_status": "Volume & Mode Rotary Dial",
                "rgb_support": "15 Built-in HW Modes & 8 Solid Colors"
            },
            "mouse": {
                "name": "Arctic Fox Wireless Mouse",
                "type": "2.4GHz Ergonomic Gaming Mouse",
                "connectivity": "2.4GHz USB Dongle",
                "rgb_support": "Onboard Cycle / DPI Indicator"
            },
            "receivers": [],
            "system_board": "Unknown"
        }

        try:
            # Query active USB dongles
            cmd = "powershell -NoProfile -Command \"Get-PnpDevice -Class USB -Status OK | Where-Object InstanceId -match '32C2' | Select-Object FriendlyName, InstanceId | ConvertTo-Json\""
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if res.stdout.strip():
                data = json.loads(res.stdout)
                if isinstance(data, dict):
                    data = [data]
                for item in data:
                    summary["receivers"].append({
                        "name": item.get("FriendlyName", "2.4G Wireless Receiver"),
                        "chipset": "OnMicro 2.4G Wireless (VID_32C2)",
                        "instance": item.get("InstanceId", "")
                    })
        except Exception:
            pass

        try:
            board_cmd = "powershell -NoProfile -Command \"(Get-CimInstance Win32_BaseBoard).Product\""
            res = subprocess.run(board_cmd, capture_output=True, text=True, timeout=5)
            if res.stdout.strip():
                summary["system_board"] = res.stdout.strip()
        except Exception:
            pass

        return summary

device_detector = DeviceDetector()
