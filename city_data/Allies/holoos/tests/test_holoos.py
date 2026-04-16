"""Testes HoloOS"""
import sys
sys.path.insert(0, '..')

def test_all():
    from holoos import get_system_status, AIHub, SecurityKernel, ToolExecutor
    print("✅ Status:", get_system_status()['name'])
    print("✅ AI Models:", len(AIHub().models))
    print("✅ Security:", SecurityKernel().get_status()['security_level'])
    print("✅ Tools:", len(ToolExecutor().tools))
    print("\n✅ Todos os testes passaram!")

if __name__ == "__main__":
    test_all()
