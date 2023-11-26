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


def create_limiting_table():
  conn = sqlite3.connect(database)
  c = conn.cursor()
  query = """create table if not exists wc_limits (
      username text,
      date text,
      chances INTEGER,
      CONSTRAINT unique_score UNIQUE(username, date)
  )"""
  c.execute(query)
  conn.commit()
  conn.close()


create_limiting_table()


def create_leaderboard_table():
  conn = sqlite3.connect(database)
  c = conn.cursor()
  query = """CREATE TABLE IF NOT EXISTS wc_leaderboard (
      username TEXT unique,
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
            user_id text unique
  )"""
  c.execute(query)
  conn.commit()
  conn.close()


create_wc_solver_list()

#------------------Solver List------------#


def add_to_wc_solvers(user_id):
  conn = sqlite3.connect(database)
  c = conn.cursor()
  query = f"""insert into wc_solvers (user_id) values ('{user_id}')"""
  c.execute(query)
  conn.commit()
  conn.close()


def get_all_wc_solvers():
  conn = sqlite3.connect(database)
  c = conn.cursor()
  query = """select user_id from wc_solvers"""
  c.execute(query)
  solvers = c.fetchall()
  return solvers


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
  cursor = conn.cursor()
  cursor.execute('SELECT score FROM wc_leaderboard WHERE username=?',
                 (username, ))
  result = cursor.fetchone()

  if result is None:
    cursor.execute(
      'INSERT INTO wc_leaderboard (username, score) VALUES (?, 1)',
      (username, ))
  else:
    current_score = result[0]
    new_score = current_score + 1
    cursor.execute('UPDATE wc_leaderboard SET score=? WHERE username=?',
                   (new_score, username))
  conn.commit()
  conn.close()


def get_leaderboard():
  conn = sqlite3.connect(database)
  c = conn.cursor()
  query = "select * from wc_leaderboard order by score desc"
  c.execute(query)
  leaderboard = c.fetchall()
  return leaderboard


#--------------Limits------------------#


def update_limits(username, date, chances):
  conn = sqlite3.connect(database)
  c = conn.cursor()
  query = f"insert or replace into wc_limits (username, date, chances) values ('{username}', '{date}', '{chances}')"
  c.execute(query)
  conn.commit()
  conn.close()


def get_chances(username, date):
  conn = sqlite3.connect(database)
  c = conn.cursor()
  query = f"select chances from wc_limits where username = '{username}' and date='{date}'"
  c.execute(query)
  chances = c.fetchone()
  try:
    return chances[0]
  except:
    return None


#--------------------Overall-----------------#
def check_solution(date, user, solution):
  chances = get_chances(user, date)
  if chances == None:
    update_limits(user, date, '4')
  chances = get_chances(user, date)
  if int(chances) > 0:
    conn = sqlite3.connect(database)
    c = conn.cursor()
    find_query = f"""select solution from weekly_challenges where date = '{date}'"""
    c.execute(find_query)
    y = c.fetchone()[0]
    y_hat = solution

    if y_hat == y:
      update_limits(user, date, '0')
      update_leaderboard(user)
      return (True, 'Congrats')
    else:
      update_limits(user, date, str(int(chances) - 1))
      return (False, 'Oopsie...That is incorrect!!!')
  else:
    return (False, 'You have used your chances for this weekly challenge')
