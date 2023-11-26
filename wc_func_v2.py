import sqlite3

database = 'database/wc_database.db'


def create_challenges_table():
  conn = sqlite3.connect(database)
  c = conn.cursor()
  query = """CREATE TABLE IF NOT EXISTS weekly_challenges (
    date TEXT unique,
    filename TEXT,
    solution TEXT
        );"""
  c.execute(query)
  conn.commit()
  conn.close()


create_challenges_table()


def create_leaderboard_table():
  conn = sqlite3.connect(database)
  c = conn.cursor()
  query = """CREATE TABLE IF NOT EXISTS wc_leaderboard (
      name TEXT unique,
      score INTEGER
  ); """
  c.execute(query)
  conn.commit()
  conn.close()


create_leaderboard_table()


def create_wc_solver_list():
  conn = sqlite3.connect(database)
  c = conn.cursor()
  query = """create table if not exists wc_solvers(
            name text unique
  )"""
  c.execute(query)
  conn.commit()
  conn.close()


create_wc_solver_list()

#------------------Solver List------------#


def get_all_wc_solvers():
  conn = sqlite3.connect(database)
  c = conn.cursor()
  query = """select name from wc_solvers"""
  c.execute(query)
  solvers = c.fetchall()
  return [(i[0]) for i in solvers]


def add_to_wc_solvers(name):
  conn = sqlite3.connect(database)
  c = conn.cursor()
  query = f"""insert into wc_solvers (name) values ('{name}')"""
  solvers = get_all_wc_solvers()

  if name not in solvers:
    c.execute(query)
    conn.commit()
  conn.close()


def remove_all_from_wc_solvers():
  conn = sqlite3.connect(database)
  c = conn.cursor()
  query = "delete from wc_solvers"
  c.execute(query)
  conn.commit()
  conn.close()


#--------------Weekly Challenges---------------#
def add_weekly_challenge(value):
  conn = sqlite3.connect(database)
  c = conn.cursor()
  query = "INSERT INTO weekly_challenges (date, filename, solution) VALUES (?,?,?)"
  try:
    c.execute(query, value)
    conn.commit()
    conn.close()
    return (f"Weekly Challenge added for date: {value[0]}")
  except:
    return ('Error occured while adding weekly challenge')
    conn.close()


def delete_weekly_challenge(date):
  conn = sqlite3.connect(database)
  c = conn.cursor()
  query = f"delete from weekly_challenges where date = '{date}'"
  try:
    c.execute(query)
    conn.commit()
    conn.close()
  except:
    conn.close()


def send_wc(date):
  conn = sqlite3.connect(database)
  c = conn.cursor()
  query = f'select filename from weekly_challenges where date = "{date}"'
  c.execute(query)
  file = c.fetchone()[0]
  return file


#---------------Leaderboard-----------------#
"""def update_leaderboard(username):
  conn = sqlite3.connect(database)
  c = conn.cursor()
  try:
    query = f"INSERT INTO wc_leaderboard (username, score) VALUES ('{username}', 1)"
    c.execute(query)
    conn.commit()
    conn.close()
  except:
    query = f"UPDATE wc_leaderboard SET score = score + 1 WHERE username='{username}';"
    c.execute(query)
    conn.commit()
    conn.close()"""


def update_leaderboard(username):
  conn = sqlite3.connect(database)
  c = conn.cursor()
  try:
    query = f"INSERT INTO wc_leaderboard (name, score) VALUES ('{username}', 1)"
    c.execute(query)
    conn.commit()
    conn.close()
  except:
    query = f"UPDATE wc_leaderboard SET score = score + 1 WHERE name='{username}';"
    c.execute(query)
    conn.commit()
    conn.close()


def get_leaderboard():
  conn = sqlite3.connect(database)
  c = conn.cursor()
  query = "select * from wc_solvers order by score desc"
  c.execute(query)
  leaderboard = c.fetchall()
  return leaderboard


#--------------------Overall-----------------#
def check_solution(date, user, solution):
  solvers = get_all_wc_solvers()
  print(solvers)
  print(user)
  if user not in solvers:
    conn = sqlite3.connect(database)
    c = conn.cursor()
    find_query = f"""select solution from weekly_challenges where date = '{date}'"""
    c.execute(find_query)
    y = c.fetchone()[0]
    y_hat = solution

    if y_hat == y:
      update_leaderboard(user)
      add_to_wc_solvers(user)
      return (True, 'Congrats')
    else:
      return (False, 'Oopsie...That is incorrect!!!')
  else:
    return (False, 'You have used your chances for this weekly challenge')
