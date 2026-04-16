import os
import time
import json
from src.core.bus import CityBus
from src.core.digital_twin import DigitalTwinEngine

class SystemTelemetry:
    """Monitor de Telemetria: Coleta dados vitais do Linux e integra ao DigitalTwin."""
    
    def __init__(self):
        self.bus = CityBus()
        self.twin = DigitalTwinEngine()
        
    def get_cpu_load(self):
        """Lê a carga de CPU do arquivo /proc/loadavg (Padrão Linux)."""
        try:
            with open("/proc/loadavg", "r") as f:
                load = f.read().split()[0]
            return float(load)
        except: return 0.0

    def get_memory_usage(self):
        """Lê o uso de memória do arquivo /proc/meminfo."""
        try:
            with open("/proc/meminfo", "r") as f:
                lines = f.readlines()
                mem_total = int(lines[0].split()[1])
                mem_free = int(lines[1].split()[1])
                mem_used = (mem_total - mem_free) / mem_total * 100
            return round(mem_used, 2)
        except: return 0.0

    def collect_and_sync(self):
        """Coleta todas as métricas e sincroniza com a réplica digital."""
        metrics = {
            "cpu_load": self.get_cpu_load(),
            "mem_usage": self.get_memory_usage(),
            "uptime": time.clock_gettime(time.CLOCK_BOOTTIME) if hasattr(time, 'CLOCK_BOOTTIME') else 0,
            "status": "Healthy"
        }
        
        # Sincroniza com o Digital Twin
        self.twin.sync_physical_to_digital("Linux_Kernel_Infrastructure", metrics)
        
        # Publica no barramento para os agentes verem
        self.bus.broadcast("Telemetry", f"Métricas de Infraestrutura: CPU {metrics['cpu_load']} | MEM {metrics['mem_usage']}%", topic="sys_health")
        return metrics

    def run_forever(self, interval=10):
        print("📊 TELEMETRY: Monitor de Infraestrutura Linux Online.")
        while True:
            self.collect_and_sync()
            time.sleep(interval)

if __name__ == "__main__":
    telemetry = SystemTelemetry()
    telemetry.run_forever()
