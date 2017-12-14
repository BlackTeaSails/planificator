def calculate_pages(current_page, last_page):
    # decidimos las paginas que añadir abajo segun las paginas totales y la pagina actual
    # se añaden las dos primeras, las dos ultimas, la actual y las dos de alrededor
    pages = [1]
    if last_page > 1:
        pages.append(2)
    if current_page>3:
        pages.append(current_page-1)
    if current_page>2:
        pages.append(current_page)
    if current_page<last_page-1 and current_page>1:
        pages.append(current_page+1)
    if current_page<last_page-1 and last_page > 3:
        pages.append(last_page-1)
    if current_page<last_page:
        pages.append(last_page)
    return pages
