import psycopg2
from config import DB_USER, DB_HOST, DB_NAME, DB_PASSWORD
from datetime import datetime


class DataBase:
    def __init__(self):
        self.database = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )

    def manager(self, sql, *args,
                fetchone: bool = False,
                fetchall: bool = False,
                fetchmany: bool = False,
                commit: bool = False):
        with self.database as db:
            with db.cursor() as cursor:
                cursor.execute(sql, args)
                if commit:
                    result = db.commit()
                elif fetchone:
                    result = cursor.fetchone()
                elif fetchall:
                    result = cursor.fetchall()
                elif fetchmany:
                    result = cursor.fetchmany()
            return result


class TableCreator(DataBase):
    def create_user_table(self):
        sql = """
            DROP TABLE IF EXISTS users;
            CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL, 
                email TEXT NOT NULL,
                description TEXT NOT NULL,
                username TEXT NOT NULL,
                team_id INT NOT NULL DEFAULT 0,
                chat_id BIGINT NOT NULL UNIQUE
            );
        """
        self.manager(sql, commit=True)

    def create_team_table(self):
        sql = """
            DROP TABLE IF EXISTS teams;
            CREATE TABLE IF NOT EXISTS teams(
                team_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                project_name TEXT NOT NULL,
                project_description TEXT,   
                who_need TEXT
            );
        """
        self.manager(sql, commit=True)

    def create_task_table(self):
        sql = """
            DROP TABLE IF EXISTS tasks;
            CREATE TABLE IF NOT EXISTS tasks(
                task_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                task_name TEXT NOT NULL,
                task_description TEXT NOT NULL,
                assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                deadline TIMESTAMP NOT NULL,
                status TEXT DEFAULT 'Открыта',
                chat_id INT DEFAULT 0,
                team_id INT NOT NULL,
                FOREIGN KEY (chat_id) REFERENCES users(chat_id) ON DELETE SET NULL,
                FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE CASCADE
            );
        """
        self.manager(sql, commit=True)


class UserManager(DataBase):
    """Работа с таблицей пользователя"""

    def get_user_id(self, chat_id):
        sql = "SELECT user_id FROM users WHERE chat_id = %s;"
        return self.manager(sql, chat_id, fetchone=True)

    def get_user_name(self, chat_id):
        sql = "SELECT name, username FROM users WHERE chat_id = %s"
        return self.manager(sql, chat_id, fetchone=True)

    def add_user(self, name, age, email, description, username, chat_id):
        sql = "INSERT INTO users(name, age, email, description, username, chat_id) VALUES (%s, %s, %s, %s, %s, %s);"
        self.manager(sql, name, age, email, description, username, chat_id, commit=True)

    def get_user_info(self, chat_id):
        sql = "SELECT name, age, email, description FROM users WHERE chat_id = %s;"
        return self.manager(sql, chat_id, fetchall=True)

    def get_user_team_id(self, chat_id):
        sql = "SELECT team_id FROM users WHERE chat_id = %s"
        return self.manager(sql, chat_id, fetchone=True)

    def get_user_team_name(self, chat_id):
        sql = """
            SELECT teams.name
            FROM teams
            JOIN users ON teams.team_id = users.team_id
            WHERE users.chat_id = %s;
        """
        return self.manager(sql, chat_id, fetchone=True)

    def change_name(self, name, chat_id):
        sql = """
            UPDATE users
            SET name = %s
            WHERE chat_id = %s
        """
        self.manager(sql, name, chat_id, commit=True)

    def change_age(self, age, chat_id):
        sql = """
            UPDATE users
            SET age = %s
            WHERE chat_id = %s
        """
        self.manager(sql, age, chat_id, commit=True)

    def change_email(self, email, chat_id):
        sql = """
            UPDATE users
            SET email = %s
            WHERE chat_id = %s
        """
        self.manager(sql, email, chat_id, commit=True)

    def change_description(self, description, chat_id):
        sql = """
            UPDATE users
            SET description = %s
            WHERE chat_id = %s
        """
        self.manager(sql, description, chat_id, commit=True)

    def add_user_into_team(self, team_id, chat_id):
        sql = """
            UPDATE users
            SET team_id = %s
            WHERE chat_id = %s
        """
        self.manager(sql, team_id, chat_id, commit=True)


class TeamManager(DataBase):
    """Работа с таблицой команд"""

    def get_team_id_by_team_name(self, team_name):
        sql = "SELECT team_id FROM teams WHERE name = %s;"
        return self.manager(sql, team_name, fetchone=True)

    def get_team_name_by_team_id(self, team_id):
        sql = "SELECT name FROM teams WHERE team_id = %s"
        return self.manager(sql, team_id, fetchone=True)

    def add_team(self, name, project, project_description, who_need, chat_id):
        sql = """
            INSERT INTO teams(name, project_name, project_description, who_need) VALUES (%s, %s, %s, %s);
        """
        self.manager(sql, name, project, project_description, who_need, commit=True)
        sql = "SELECT team_id FROM teams WHERE name = %s"
        team_id = self.manager(sql, name, fetchone=True)[0]
        sql = """
            UPDATE users 
            SET team_id = %s
            WHERE chat_id = %s
        """
        self.manager(sql, team_id, chat_id, commit=True)

    def show_team(self, user_id):
        sql = """
            SELECT name FROM teams
            JOIN users ON users.team_id = teams.team_id 
            WHERE users.user_id = %s
        """
        return self.manager(sql, user_id, fetchall=True)

    def show_team_info(self, team_id):
        sql = """
            SELECT 
                teams.name AS team_name,
                DATE(teams.created_at) AS created_date,
                teams.project_name,
                teams.project_description,
                teams.who_need,
                COUNT(users.user_id) AS user_count
            FROM 
                teams
            LEFT JOIN 
                users ON users.team_id = teams.team_id
            WHERE 
                teams.team_id = %s
            GROUP BY 
                teams.team_id, 
                teams.name, 
                DATE(teams.created_at), 
                teams.project_name, 
                teams.project_description, 
                teams.who_need;
        """
        return self.manager(sql, team_id, fetchone=True)

    def delete_user_from_team(self, user_id):
        sql = """
            UPDATE users
            SET team_id = 0
            WHERE user_id = %s;
        """
        self.manager(sql, user_id, commit=True)

    def need_delete_team(self, team_id):
        sql = """
            SELECT COUNT(user_id) FROM users
            WHERE team_id = %s
        """
        return self.manager(sql, team_id, fetchone=True)

    def finally_delete_team(self, team_id):
        sql = """
            DELETE FROM teams
            WHERE team_id = %s
        """
        self.manager(sql, team_id, commit=True)

    def get_teams_info_without_user(self, chat_id):
        sql = """
            SELECT teams.name, teams.project_name, teams.project_description, teams.who_need
            FROM teams
            WHERE team_id NOT IN (
                SELECT team_id
                FROM users
                WHERE chat_id = %s
            );
        """
        return self.manager(sql, chat_id, fetchall=True)

    def get_team_name(self, chat_id):
        sql = """
            SELECT teams.name FROM teams
            WHERE team_id NOT IN(
                SELECT team_id
                FROM users
                WHERE chat_id = %s);
        """
        return self.manager(sql, chat_id, fetchall=True)

    def get_members(self, team_id):
        sql = """
            SELECT users.name, users.username FROM users
            JOIN teams ON teams.team_id = users.team_id
            WHERE teams.team_id = %s;
        """
        return self.manager(sql, team_id, fetchall=True)


class TaskManager(DataBase):
    """Работа с таблицой задач"""

    def add_task(self, task_name, task_description, deadline, team_id):
        sql = """
            SET session_replication_role = 'replica';
            INSERT INTO tasks(task_name, task_description, deadline, team_id)
            VALUES (%s, %s, %s, %s);
            SET session_replication_role = 'origin';
        """
        self.manager(sql, task_name, task_description, deadline, team_id, commit=True)

    def task_by_user(self, chat_id):
        sql = """
            SELECT task_name, task_description, assigned_at, deadline FROM tasks
            WHERE chat_id = %s
        """
        return self.manager(sql, chat_id, fetchone=True)

    def task_by_team(self, team_id):
        sql = """
            SELECT task_name, task_description, status FROM tasks
            WHERE team_id = %s
        """
        return self.manager(sql, team_id, fetchall=True)

    def get_task_info(self, task_id, team_id):
        sql = """
            SELECT task_name, task_description, assigned_at, deadline, status, chat_id
            FROM tasks
            WHERE task_id = %s AND team_id = %s
        """
        return self.manager(sql, task_id, team_id, fetchone=True)

    def get_task_id_by_task_name(self, task_name):
        sql = "SELECT task_id FROM tasks WHERE task_name = %s"
        return self.manager(sql, task_name, fetchone=True)

    def get_task_name_by_chat_id(self, chat_id):
        sql = "SELECT task_name FROM tasks WHERE chat_id = %s"
        return self.manager(sql, chat_id, fetchone=True)

    def get_task_user(self, chat_id):
        sql = "SELECT task_id FROM tasks WHERE chat_id = %s"
        return self.manager(sql, chat_id, fetchone=True)

    def update_user_dont_have_task(self, task_id):
        sql = """
            SET session_replication_role = 'replica';
            UPDATE tasks 
            SET chat_id = 0 
            WHERE task_id = %s;
            SET session_replication_role = 'origin';
        """
        self.manager(sql, task_id, commit=True)

    def update_user_accept(self, chat_id, task_id):
        sql = """
            SET session_replication_role = 'replica';
            UPDATE tasks 
            SET chat_id = %s 
            WHERE task_id = %s;
            SET session_replication_role = 'origin';
        """
        self.manager(sql, chat_id, task_id, commit=True)

    def delete_task_line(self, task_id):
        sql = """
            DELETE FROM tasks
            WHERE task_id = %s
        """
        self.manager(sql, task_id, commit=True)


class MainManager:
    def __init__(self):
        self.user: UserManager = UserManager()
        self.team: TeamManager = TeamManager()
        self.task: TaskManager = TaskManager()


creator = TableCreator()
# creator.create_team_table()
# creator.create_user_table()
# creator.create_task_table()

