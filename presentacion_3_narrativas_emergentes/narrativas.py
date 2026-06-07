import random
from dataclasses import dataclass, field

NAMES = [
    "Ana", "Luis", "Marta", "Sofía", "Diego",
    "Elena", "Pablo", "Lucía", "Carlos", "Nora"
]

TRAITS = [
    "amable", "desconfiado", "valiente", "egoísta",
    "curioso", "impulsivo", "paciente", "generoso"
]

PLACES = ["la plaza", "el mercado", "la aldea", "el bosque", "las ruinas"]


@dataclass
class Agent:
    name: str
    trait: str
    hunger: int = field(default_factory=lambda: random.randint(0, 100))
    trust: int = field(default_factory=lambda: random.randint(20, 80))
    mood: int = field(default_factory=lambda: random.randint(20, 80))
    energy: int = field(default_factory=lambda: random.randint(20, 100))

    def short_state(self) -> str:
        return (
            f"hambre={self.hunger}, confianza={self.trust}, "
            f"ánimo={self.mood}, energía={self.energy}"
        )

    def update_after_step(self):
        self.hunger = min(100, self.hunger + random.randint(3, 12))
        self.energy = max(0, self.energy - random.randint(2, 10))
        self.mood = max(0, min(100, self.mood + random.randint(-6, 6)))


def create_agents(n: int = 5) -> list[Agent]:
    names = random.sample(NAMES, k=n)
    traits = random.choices(TRAITS, k=n)
    return [Agent(name=names[i], trait=traits[i]) for i in range(n)]


def interaction(a: Agent, b: Agent) -> str:
    """
    Genera una interacción narrativa basada en rasgos y estados.
    """
    place = random.choice(PLACES)

    # Reglas simples para elegir el tipo de interacción
    if a.hunger > 75 and b.hunger > 75:
        a.trust -= 5
        b.trust -= 5
        a.mood -= 4
        b.mood -= 4
        return f"En {place}, {a.name} y {b.name} discuten por la última comida."

    if a.hunger > 70 and b.trust > 55:
        a.hunger = max(0, a.hunger - 20)
        a.trust += 6
        b.trust += 4
        a.mood += 5
        b.mood += 3
        return f"En {place}, {b.name} comparte comida con {a.name}, y la relación entre ambos mejora."

    if a.trait == "egoísta" and random.random() < 0.4:
        b.trust -= 8
        a.trust -= 2
        a.mood += 2
        return f"En {place}, {a.name} oculta información a {b.name}, generando desconfianza."

    if a.trait == "generoso" or b.trait == "generoso":
        a.trust += 4
        b.trust += 4
        a.mood += 3
        b.mood += 3
        return f"En {place}, {a.name} y {b.name} colaboran para resolver un problema del grupo."

    if a.trait == "impulsivo" and random.random() < 0.5:
        b.mood -= 6
        a.mood -= 2
        return f"En {place}, {a.name} interrumpe a {b.name} de forma brusca y crea tensión."

    if a.energy < 25:
        a.mood -= 3
        a.trust += 2
        return f"En {place}, {a.name} apenas tiene energía y pide ayuda a {b.name}."

    # Interacción neutra por defecto
    a.trust += 1
    b.trust += 1
    a.mood += 1
    b.mood += 1
    return f"En {place}, {a.name} y {b.name} conversan y mantienen una relación estable."


def clamp_stats(agent: Agent):
    agent.hunger = max(0, min(100, agent.hunger))
    agent.trust = max(0, min(100, agent.trust))
    agent.mood = max(0, min(100, agent.mood))
    agent.energy = max(0, min(100, agent.energy))


def run_simulation(num_agents: int = 5, steps: int = 10, seed: int | None = None):
    if seed is not None:
        random.seed(seed)

    agents = create_agents(num_agents)

    print("=== INICIO DE LA SIMULACIÓN ===")
    print("Personajes iniciales:")
    for agent in agents:
        print(f"- {agent.name} ({agent.trait}): {agent.short_state()}")
    print()

    for step in range(1, steps + 1):
        print(f"--- Paso {step} ---")

        a, b = random.sample(agents, 2)
        narration = interaction(a, b)
        print(narration)

        # Actualización del estado interno de todos los agentes
        for agent in agents:
            agent.update_after_step()
            clamp_stats(agent)

        print("Estado del mundo:")
        for agent in agents:
            print(f"- {agent.name}: {agent.short_state()}")
        print()

    print("=== FIN DE LA SIMULACIÓN ===")


if __name__ == "__main__":
    run_simulation(num_agents=5, steps=12, seed=42)
