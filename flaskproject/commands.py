from models import BoardModel, PostModel, UserModel
from exts import db
import random


def init_boards():
    board_names = ['公开/public','私有/private']
    for index, board_name in enumerate(board_names):
        board = BoardModel(name=board_name,priority=len(board_names)-index)
        db.session.add(board)
    db.session.commit()
    print("板块初始化成功！")


def create_test_posts():
    boards = list(BoardModel.query.all())
    board_count = len(boards)
    for x in range(9):
        title = "我是标题%d"%x
        content = "我是内容%d"%x
        author = UserModel.query.first()
        index = random.randint(0,board_count-1)
        board = boards[index]
        post_model = PostModel(title=title,content=content,author=author,board=board)
        db.session.add(post_model)
    db.session.commit()
    print("测试帖子添加成功")