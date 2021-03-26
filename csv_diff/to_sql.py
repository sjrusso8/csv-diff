import itertools


def diff_alter_drop(values, table):
    sql = []
    seperater = ""

    sql.append(f'ALTER TABLE {table}')

    if len(values) > 1:
        seperater = ","

    for i, v in enumerate(values):
        if i == len(values) - 1:
            seperater = ";"

        sql.append(f'DROP COLUMN IF EXISTS {v}' + seperater)

    return ' '.join([v for v in sql])


def diff_alter_add(values, table):
    sql = []
    seperater = ""

    sql.append(f'ALTER TABLE {table}')

    if len(values) > 1:
        seperater = ","

    for i, v in enumerate(values):
        if i == len(values) - 1:
            seperater = ";"

        sql.append(f'ADD COLUMN {v} VARCHAR(250)' + seperater)

    return ' '.join([v for v in sql])


def diff_insert(values, table):
    sql = []
    seperater = ","
    columns = [list(x) for x in set(tuple(k.keys()) for k in values)][0]

    sql.append(f'INSERT INTO TABLE {table} ' +
               '(' + ', '.join([v for v in columns]) + ')')
    sql.append('VALUES')

    for i, v in enumerate(values):

        if i == len(values) - 1:
            seperater = ";"

        added_values = ', '.join(map(str,  list(v.values())))
        sql.append(f'({added_values}){seperater}')
    return sql


def diff_delete(values, table, key):
    sql = []
    ids = ', '.join(map(str, [x[key] for x in values]))

    sql.append(f'DELETE FROM {table} WHERE {key} IN ({ids});')

    return sql


def diff_update(values, table, key):
    sql = []

    for _, v in enumerate(values):
        statement = f'''UPDATE {table} SET '{''.join(list(v['changes'].keys()))}' = {list(v['changes'].values())[0][1]} WHERE {key} = {v['key']};'''
        sql.append(statement)
    return sql


def diff_to_sql(diff, table, key):
    sql = []
    for k, v in diff.items():
        if k == 'columns_added':
            sql.append(diff_alter_add(v, table))
        if k == 'columns_removed':
            sql.append(diff_alter_drop(v, table))
        if k == 'added':
            sql.append(diff_insert(v, table))
        if k == 'removed':
            sql.append(diff_delete(v, table, key))
        if k == 'changed':
            sql.append(diff_update(v, table, key))
    return list(itertools.chain(*sql))
