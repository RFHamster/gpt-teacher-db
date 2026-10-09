from enum import Enum


class TeachingMethodology(str, Enum):
    """Metodologia de ensino aplicada nas respostas da IA para o aluno"""

    SOCRATIC = "socratic"          # nunca corrige, só pergunta
    DIRECT = "direct"              # aponta o erro e explica diretamente
    STEP_BY_STEP = "step_by_step"  # guia o aluno passo a passo até a solução