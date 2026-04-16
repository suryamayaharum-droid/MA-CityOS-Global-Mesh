import asyncio
from src.agents.openclaude_bridge import OpenClawBridge

class CognitiveSwarm:
    """Motor de Paralelismo Cognitivo: Faz vários agentes pensarem ao mesmo tempo."""
    
    def __init__(self):
        self.bridge = OpenClawBridge()
        
    async def think_parallel(self, task, perspectives):
        """
        Executa a mesma tarefa sob diferentes perspectivas simultaneamente.
        Ex: Um agente focado em 'Segurança', outro em 'Performance', outro em 'Criatividade'.
        """
        print(f"🐝 SWARM: Iniciando Paralelismo Cognitivo para: '{task[:30]}...'")
        
        async def agent_thought(persona, task):
            print(f"   -> Instanciando pensamento: {persona}")
            # Em um cenário real assíncrono, a bridge precisaria de um cliente Async
            # Aqui simulamos o wrapper assíncrono para a ponte síncrona atual
            response = await asyncio.to_thread(
                self.bridge.ask_agent, 
                task, 
                system_instruction=f"Você é um especialista focado ESTRITAMENTE em: {persona}. Analise a tarefa sob essa ótica."
            )
            return {"persona": persona, "insight": response}

        # Cria as tarefas e as roda todas de uma vez!
        tasks = [agent_thought(p, task) for p in perspectives]
        results = await asyncio.gather(*tasks)
        
        print("🧠 SWARM: Convergência de pensamentos concluída.")
        return results

if __name__ == "__main__":
    swarm = CognitiveSwarm()
    perspectives = ["Segurança Cibernética", "Eficiência de Código", "Impacto Social"]
    insights = asyncio.run(swarm.think_parallel("Devemos conectar o MA-CityOS a redes blockchain abertas?", perspectives))
    for i in insights:
        print(f"\n--- Ótica: {i['persona']} ---")
        print(i['insight'][:150] + "...")
