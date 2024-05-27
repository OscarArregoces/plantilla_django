
def menuResources(data: list, list_data: list, model, last_id: int, id_padre=0):
    id_last_resources = last_id
    method = "GET"
    

    for i in data:
        if "method" in i: 
                method = i["method"]
        
        if id_padre != 0:
            id_padre_resource = i["id_padre"] if "id_padre" in i else id_padre
            
            list_data.append(model(
                path=i['path'], link=i['link'], icono=i['icono'], method=method, titulo=i['titulo'], id_padre=id_padre_resource, id=list_data[-1].id + 1))
        else:
            id = last_id if len(list_data) == 0 else list_data[-1].id + 1
            id_padre = i['id_padre'] if 'id_padre' in i else 0
            list_data.append(model(
                path=i['path'], link=i['link'], icono=i['icono'], method=method, titulo=i['titulo'], id_padre=id_padre, id=id))
        id_last_resources += 1
        if 'items' in i:
            menuResources(data=i['items'], list_data=list_data, model=model,
                          last_id=id_last_resources, id_padre=list_data[-1].id)
    return list_data
