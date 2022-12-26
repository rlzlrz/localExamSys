import dao, logging, configure, random

def addUser(account: str, passwd: str) -> bool:
    x = dao.userlist.find_one({'account': account})
    if x is not None:
        logger.info('account exists!')
        return False
    else:
        dao.userlist.insert_one({'account': account, 'passwd': passwd})
        logger.info('new user added successfully!')
        return True

def authCheck(account: str, passwd: str) -> bool:
    x = dao.userlist.find_one({'account': account})
    if x is None:
        logger.info('bad account or passwd!')
        return False
    else:
        if x['passwd'] != passwd:
            logger.info('bad account or passwd!')
            return False
        else:
            logger.info('loggin success!')
            return True

def registCheck(account: str) -> bool:
    if len(account) < 6:
        return False
    x = dao.userlist.find_one({'account': account})
    if x is None:
        logger.info('account not used!')
        return True
    return False

def randomQuestions() -> list:
    questionList = []
    target = [i for i in range(1, 10001)]
    numList = random.sample(target, configure.EXAM_COUNT)
    for i in range(0, configure.EXAM_COUNT):
        question = dao.mycol.find_one({'_id': numList[i]})
        question['count'] = i
        questionList.append(question)
    return questionList


class backEnd:
    Questions = []

    def __init__(self):
        self.getQuestions()

    def getQuestions(self):
        self.Questions = randomQuestions()


logger = logging.getLogger('[LOGGER]')
console_handler = logging.StreamHandler()
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

if __name__ == '__main__':
    b1 = backEnd()
    count = 0
    for i in b1.Questions:
        print(i)
        count += 1
    print(count)
    
    logger.info('You should run frontend.py, not this one!')