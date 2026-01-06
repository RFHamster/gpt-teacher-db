import re

import requests


def validate_cpf(cpf: str) -> bool:
    """
    Valida um número de CPF (Cadastro de Pessoas Físicas) brasileiro.

    Args:
        cpf: A string do CPF a ser validada. Pode conter pontos e traço.

    Returns:
        True se o CPF for válido, False caso contrário.
    """
    # Remove caracteres não numéricos
    cpf_digits = re.sub(r"\D", "", cpf)

    # Verifica se possui 11 dígitos
    if len(cpf_digits) != 11:
        return False

    # Verifica se todos os dígitos são iguais (ex: 111.111.111-11)
    if len(set(cpf_digits)) == 1:
        return False

    # Calcula o primeiro dígito verificador
    sum_ = sum(int(cpf_digits[i]) * (10 - i) for i in range(9))
    remainder = (sum_ * 10) % 11
    digit1 = remainder if remainder < 10 else 0
    if digit1 != int(cpf_digits[9]):
        return False

    # Calcula o segundo dígito verificador
    sum_ = sum(int(cpf_digits[i]) * (11 - i) for i in range(10))
    remainder = (sum_ * 10) % 11
    digit2 = remainder if remainder < 10 else 0
    if digit2 != int(cpf_digits[10]):
        return False

    return True


def mask_cpf(cpf: str) -> str:
    """
    Formata uma string de CPF para o padrão XXX.XXX.XXX-XX.

    Args:
        cpf: A string do CPF, contendo apenas dígitos ou já formatada.

    Returns:
        A string do CPF formatada no padrão XXX.XXX.XXX-XX.

    Raises:
        ValueError: Se o CPF, após remover caracteres não numéricos,
                    não contiver exatamente 11 dígitos.
    """
    # Remove caracteres não numéricos
    cpf_digits = re.sub(r"\D", "", cpf)

    # Verifica se possui 11 dígitos
    if len(cpf_digits) != 11:
        raise ValueError("CPF inválido. Deve conter exatamente 11 dígitos.")

    # Aplica a formatação
    return f"{cpf_digits[:3]}.{cpf_digits[3:6]}.{cpf_digits[6:9]}-{cpf_digits[9:]}"


def format_cpf(cpf: str) -> str:
    """
    Remove a formatação de uma string de CPF, retornando apenas os dígitos.

    Args:
        cpf: A string do CPF formatado (ex: XXX.XXX.XXX-XX) ou já sem formatação.

    Returns:
        Uma string com apenas os 11 dígitos do CPF.

    Raises:
        ValueError: Se, após a remoção dos caracteres não numéricos,
                    o CPF não tiver exatamente 11 dígitos.
    """
    # Remove tudo que não for dígito
    cpf_digits = re.sub(r"\D", "", cpf)

    if len(cpf_digits) != 11:
        raise ValueError("CPF inválido. Deve conter exatamente 11 dígitos.")

    return cpf_digits


def validate_cep_online(cep: str):
    """
    Valida o CEP usando a API pública BrasilAPI.
    """
    cep_digits = re.sub(r"\D", "", cep)
    if len(cep_digits) != 8:
        return False

    return requests.get(f"https://brasilapi.com.br/api/cep/v1/{cep_digits}")


def format_cep(cep: str) -> str:
    """
    Formata o CEP no padrão XXXXX-XXX.
    """
    cep_digits = re.sub(r"\D", "", cep)
    if len(cep_digits) != 8:
        raise ValueError("CEP inválido. Deve conter exatamente 8 dígitos.")
    return cep_digits


from datetime import date


def validate_date_of_birth(date_of_birth: date, max_age: int = 120) -> bool:
    """
    Valida uma data de nascimento do tipo `date`.

    Args:
        date_of_birth: A data de nascimento.

    Returns:
        True se a data for válida, False caso contrário.
    """
    today = date.today()

    if date_of_birth >= today:
        return False

    age = (
        today.year
        - date_of_birth.year
        - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    )

    return 0 <= age <= max_age
