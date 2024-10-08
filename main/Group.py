
def create_group(group_name, groups):
    if group_name in groups:
        return "Erro, grupo já existente"
    groups[group_name] = []
    print(f'create: {groups.keys()}')
    return f"Grupo {group_name} adicionado"

def list_groups(groups):
    if not groups:
        return "Erro, nenhum grupo cadastrado"
    print(f'list: {groups.keys()}')
    return list(groups.keys())

def list_users_groups(group_name, groups):
    if group_name in groups:
        return groups[group_name]
    return "Erro, nenhum grupo cadastrado"

def join_group(group_name, groups, person_name):
    if group_name in groups:
        if person_name in groups[group_name]:
            return f"Erro, {person_name} já está cadastrado no grupo {group_name}"
        print(f'dentro do metodo join. | {person_name}, {group_name}, {groups[group_name]}')
        groups[group_name] = groups[group_name] + [person_name]
        print(f'join: --------- {groups[group_name]}')
        return f"{person_name} adicionado no grupo {group_name}"
    return "Erro, nenhum grupo cadastrado"

def leave_group(group_name, groups, person_name):
    if group_name in groups:
        if person_name in groups[group_name]:
            list_groups = list(groups[group_name])
            list_groups.remove(person_name)
            groups[group_name] = list_groups
            return f"{person_name} foi removido(a) do grupo {group_name}"
        return f"Erro, {person_name} não está cadastrado(a) no grupo {group_name}"
    return "Erro, nenhum grupo cadastrado"