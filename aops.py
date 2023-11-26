import sqlite3

database = 'database/aops.db'


def give_category():
  with sqlite3.connect(database) as conn:
    cursor = conn.cursor()
    query = """
            SELECT distinct category FROM aops;
            """
    try:
      cursor.execute(query)
      data = cursor.fetchall()
      category = [i[0] for i in data]
      return category
    except:
      return "No category found."


def give_contest(category):
  with sqlite3.connect(database) as conn:
    cursor = conn.cursor()
    query = f"""
            SELECT distinct contest FROM aops where category='{category}'
            """
    try:
      cursor.execute(query)
      data = cursor.fetchall()
      contests = [i[0] for i in data]
      return contests
    except:
      return 'No contest found for the given category...'


def give_sub_contest(contest):
  with sqlite3.connect(database) as conn:
    cursor = conn.cursor()
    query = f"""
            SELECT distinct name FROM aops where contest='{contest}'
            """
    try:
      cursor.execute(query)
      data = cursor.fetchall()
      events = [i[0] for i in data]
      return events
    except:
      return 'No events found for the given contest...'


def give_problem(name, year, which):
  with sqlite3.connect(database) as conn:
    cursor = conn.cursor()
    query = f"""
           select problem_html from aops
           where (name = '{year} {name}' or name = '{name} {year}') and which like '%{which}%';
            """
    try:
      cursor.execute(query)
      data = cursor.fetchone()[0]
    except:
      data = 'No problem found for the given queries'
    return data


def give_solution(name, year, which, index=1):
  """returns like, solution_html"""
  with sqlite3.connect(database) as conn:
    cursor = conn.cursor()
    query = f"""
           select solution_{index} from aops
          where (name = '{year} {name}' or name = '{name} {year}') and which like '%{which}%';
            """
    try:
      cursor.execute(query)
      data = cursor.fetchone()[0]
    except:
      data = 'No solution found for the given queries'
    return data


def random_prob(what=None):
  """returns name, problem, problem_html"""
  with sqlite3.connect(database) as conn:
    cursor = conn.cursor()
    try:
      if what == None:
        query = """
                select name, which, problem_html from aops 
                order by random() limit 1;
                """
        cursor.execute(query)
        data = cursor.fetchone()

      else:
        query = f"""
                select name, which, problem_html from aops 
                where
                category like '%{what}%' or contest like '%{what}%' or name like '%{what}%'
                order by random() limit 1;
                """
        cursor.execute(query)
        data = cursor.fetchone()
    except:
      data = ['', 'Something is not working...']
    return data
