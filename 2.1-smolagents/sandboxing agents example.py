# Set up secure code execution environment
from smolagents import CodeAgent
from e2b import Sandbox

sandbox = Sandbox(
    allowed_imports=["math", "random", "datetime"],  # Limitar importaciones
    network_access=False,  # Deshabilitar acceso a la red
    filesystem_access=False,  # Bloquear acceso al sistema de archivos
)

agent = CodeAgent(
    tools=[],
    model="gpt-4",
    additional_authorized_imports=['datetime'],
    sandbox=sandbox,  # Integrar el sandbox en el agente
    execution_timeout=5,  # Limitar tiempo de ejecución
    memory_limit=128  # Limitar memoria usada
)