
def create_group(group_name, groups):
    if group_name in groups:
        return "Erro, grupo já existente"

    groups[group_name] = []
    return f"Grupo {group_name} adicionado"


def list_groups(groups):
    if not groups:
        return "Erro, nenhum grupo cadastrado"

    return list(groups.keys())


def list_users_groups(group_name, groups):
    if group_name in groups:
        return groups[group_name]

    return "Erro, nenhum grupo cadastrado"


def join_group(group_name, groups, person_name):
    if group_name in groups:
        groups[group_name].append(person_name)
        if person_name in groups[group_name]:
            return f"Erro, {person_name} já está cadastrado no grupo {group_name}"
        return f"{person_name} adicionado no grupo {group_name}"
    return "Erro, nenhum grupo cadastrado"


def leave_group(group_name, groups, person_name):
    if group_name in groups:
        if person_name in groups[group_name]:
            groups[group_name].remove(person_name)
            return f"{person_name} foi removido(a) do grupo {group_name}"
        return f"Erro, {person_name} não está cadastrado(a) no grupo {group_name}"
    return "Erro, nenhum grupo cadastrado"

