import discord
import cogs.helper as helper
import random
from discord.ext import commands

class games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def discord_input(self, listen): # listen: from who to listen from
        return str((await self.bot.wait_for('message', timeout=180.0, check = lambda msg: msg.author == listen)).content)
    
    @commands.command(name='hangman', help='Plays a hangman game! Code contributed by Rory.')
    async def hangman(self, ctx):
        helper.log_event(str(ctx.author) + ' has started a game of hangman.')
        HANGMAN_PICS = ['''
          +---+
              |
              |
              |
             ===''', '''
          +---+
          O   |
              |
              |
             ===''', '''
          +---+
          O   |
          |   |
              |
             ===''', '''
          +---+
          O   |
         /|   |
              |
             ===''', '''
          +---+
          O   |
         /|\  |
              |
             ===''', '''
          +---+
          O   |
         /|\  |
         /    |
             ===''', '''
          +---+
          O   |
         /|\  |
         / \  |
             ===''','''
          +---+
         [O   |
         /|\  |
         / \  |
             ===''','''
          +---+
         [O]  |
         /|\  |
         / \  |
             ===''']

        words = {'Colors':'red orange yellow green blue indigo violet white black brown cyan magenta grey turquois '.split(),
                 'Shapes':'square triangle rectangle circle ellipse rhombus trapezoid chevron pentagon hexagon septagon octagon'.split(),
                 'Food':'burger fries pizza sandwich pineapple cheese sushi food apple orange lemon lime pear watermelon grape grapefruit cherry banana cantaloupe mango strawberry tomato'.split(),
                 'Animals':'ant baboon badger bat bear beaver camel cat clam cobra cougar coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk lion lizard llama mole monkey moose mouse mule newt otter owl panda parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep skunk sloth snake spider stork swan tiger toad trout turkey turtle weasle whale wolf wombat zebra'.split()}

        def getRandomWord(wordDict):
            wordKey = random.choice(list(wordDict.keys()))
            wordIndex = random.randint(0, len(wordDict[wordKey]) - 1)
            return [wordDict[wordKey][wordIndex], wordKey]
         

        async def displayBoard(missedLetters, correctLetters, secretWord):
            DBdisplaystr = '```'
            DBdisplaystr = DBdisplaystr + HANGMAN_PICS[len(missedLetters)] + '\nMissed letters: '
            for letter in missedLetters:
                DBdisplaystr = DBdisplaystr + letter + ' '
            DBdisplaystr = DBdisplaystr + '\n'
            blanks = '_' * len(secretWord)
         
            for i in range(len(secretWord)):
                if secretWord[i] in correctLetters:
                    blanks = blanks[:i] + secretWord[i] + blanks[i+1:]
         
            for letter in blanks:
                DBdisplaystr = DBdisplaystr + letter + ' '
            DBdisplaystr = DBdisplaystr + '```\n'
    #         print(DBdisplaystr)
            await ctx.send(DBdisplaystr)
         
        async def getGuess(alreadyGuessed):
            while True:
                await ctx.send('Guess a letter')    
                guess = str((await self.bot.wait_for('message', timeout=180.0, check=lambda msg: msg.author == ctx.author)).content)
                guess = guess.lower()
                if guess == 'quit':
                    return 'quit'
                elif len(guess) != 1:
                    await ctx.send('Please enter a single letter')
                elif guess in alreadyGuessed:
                    await ctx.send('You have already gussed that letter. Choose again.')
                elif guess not in 'qwertyuiopasdfghjklzxcvbnm':
                    await ctx.send('Please enter a LETTER')
                else:
                    return guess
         
        async def playAgain():
            await ctx.send('Do you want to play again ( yes/no )')
            return str((await self.bot.wait_for('message', timeout=180.0, check=lambda msg: msg.author == ctx.author)).content).lower().startswith('y')
         
        await ctx.send('H A N G M A N - **Code contributed by Rory**') 

        difficulty = 'X'
        while difficulty not in 'EMH':
            await ctx.send('Enter difficulty: E - Easy, M - Medium, H - Hard')
            difficulty = str((await self.bot.wait_for('message', timeout=180.0, check=lambda msg: msg.author == ctx.author)).content).upper()
    #         print(difficulty)
        if difficulty == 'M':
            del HANGMAN_PICS[8]
            del HANGMAN_PICS[7]
        if difficulty == 'H':
            del HANGMAN_PICS[8]
            del HANGMAN_PICS[7]
            del HANGMAN_PICS[5]
            del HANGMAN_PICS[3]
           
        missedLetters = ''
        correctLetters = ''
        secretWord, secretSet = getRandomWord(words)
        gameIsDone = False
         
        while True:
            await ctx.send(str('The secret word is in the set: '+ secretSet))
            await displayBoard(missedLetters, correctLetters, secretWord)
         
            guess = await getGuess(missedLetters + correctLetters)
            if guess == 'quit':
                await ctx.send('Your game has ended.')
                helper.log_event(str(ctx.author) + ' has ended their hangman game.')
                return
    #         print(guess)
            if guess in secretWord:
                correctLetters = correctLetters+guess
         
                foundAllLetters = True
                for i in range(len(secretWord)):
                    if secretWord[i] not in correctLetters:
                        foundAllLetters = False
                        break
                if foundAllLetters:
                    await ctx.send('Yes! The secret word is "'+secretWord+'"! You have won!')
                    gameIsDone = True
                   
            else:
                 missedLetters = missedLetters+guess
         
                 if len(missedLetters) == len(HANGMAN_PICS) - 1:
                     await displayBoard(missedLetters, correctLetters, secretWord)
                     await ctx.send('You have run out of guesses!\nAfter '+str(len(missedLetters))+' missed guesses and '+str(len(correctLetters))+' correct guesses, the word was "'+secretWord+'"')
                     gameIsDone = True
            if gameIsDone:
                if await playAgain():
                      missedLetters = ''
                      correctLetters = ''
                      gameIsDone = False
                      secretWord, secretSet = getRandomWord(words)
                else:
                    break
        helper.log_event(str(ctx.author) + ' has finished their hangman game.')
        await ctx.send('Nice playing with you! (Game exited)')

    @commands.command(name='greedypigs', help='obama greedypigs. Roll two dice! First to get to 100 points wins! But be careful, rolling sixes are really bad...')
    async def greedypigs(self, ctx):
        targets = []
        psum = []
        players = None
        choice = None
        async def determinePlayers():
            nonlocal choice
            nonlocal players
            nonlocal targets
            while(choice not in 'A B QUIT'.split()): # maybe add a quit option???
                await ctx.send('Choose an option:```\nA: Vs. Your own account\nB: Vs Other Discord Users```')
                print(ctx.author)
                choice = str(await games.discord_input(self, ctx.author)).upper()
            if(choice == 'A'):
                await ctx.send('You will be entering input from only your current account.\n\nHow many players?')
                while(not isinstance(players, int)):
                    try:
                        players = int(await games.discord_input(self, ctx.author))
                    except:
                        await ctx.send('You need to enter an integer!')
                        pass
                await ctx.send(f'Great! The game will be played with only your account with **{players}** players!')
                for i in range(players):
                    targets.append(ctx.author)
                    psum.append(0)
            if(choice == 'B'):
                await ctx.send('You will be playing this game with multiple different discord users.\n\nHow many players?')
                while(not isinstance(players, int)):
                    try:
                        players = int(await games.discord_input(self, ctx.author))
                    except:
                        await ctx.send('You need to enter an integer!')
                        pass
                await ctx.send(f'Great! The game will be played with **{players}** discord users.\nYou will be player 1.')
                targets.append(ctx.author)
                psum.append(0)
                for i in range(1, players):
                    await ctx.send(f'Ping player {i + 1}!')
                    while(True):
                        inp = await games.discord_input(self, ctx.author)
                        if(inp.lower() == 'quit'):
                            return 'quit'
                        try:
                            targetid = int(get_id(inp))
                            target = await self.bot.fetch_user(targetid)
                            if(target != None):
                                targets.append(target)
                                psum.append(0)
                                break
                        except:
                            pass
                        ctx.send('I couldn\'t find that user! Try again, or type \"quit\".')
            if(choice == 'QUIT'):
                return 'quit'
        def dice():
            return random.randint(1, 6)
        def printScore():
            scorestring = ''
            for i in range(players):
                scorestring = scorestring + f'Player {i + 1}: {psum[i]}\n'
            return('```\n--------------------\n' + scorestring + '--------------------\n```')
        async def playGame():
            rand1 = 0
            rand2 = 0
            turn = -1
            pcsum = 0
            finshed = -1
            inp = ''
            outp = ''
            detpstatus = await determinePlayers()
            if(detpstatus == 'quit'):
                return 'quit'
            while(True):
                pcsum = 0
                turn = (turn + 1) % players
    #             await ctx.send(f'IT IS NOW PLAYER {turn + 1}\'S TURN')
                outp = f'IT IS NOW PLAYER {turn + 1}\'S TURN\n'
                while(True):
                    outp = outp + 'Initial roll: \n'
    #                 await ctx.send('Initial roll: ')
                    rand1 = dice()
                    rand2 = dice()
                    outp = outp + f'You rolled `{rand1}`, `{rand2}`.\n'
    #                 await ctx.send(f'You rolled {rand1}, {rand2}.')
                    if(not(rand1 == 6 or rand2 == 6)):
                        break
                    outp = outp + 'At least one of the two dice was six, rerolling...\n'
    #                 await ctx.send('At least one of the two dice was six, rerolling...')
                await ctx.send(outp)
                pcsum += rand1 + rand2
                while(True):
                    if(psum[turn] + pcsum >= 100):
                        psum[turn] += pcsum
                        await ctx.send(f'**GAME OVER**\n\nPlayer {turn + 1} has reached 100! The scores are as follows: {printScore()}')
                        return
                    await ctx.send(f'You have {psum[turn]} points from before, and {pcsum} points this round.\n{targets[turn].mention} it is your turn to make an input: you can \"stand\" or \"hit\".')
                    inp = ''
                    while(not(inp.startswith('s') or inp.startswith('h'))):
                        await ctx.send('Enter hit or stand. (or quit)')
                        inp = str(await games.discord_input(self, targets[turn])).lower()
                        if(inp == 'quit'):
                            return 'quit'
                    if(inp.startswith('s')):
                        break
                    rand1 = dice()
                    rand2 = dice()
                    outp = f'{targets[turn].mention} have rolled `{rand1}` and `{rand2}`.'
    #                 await ctx.send(f'{targets[turn].mention} have rolled `{rand1}` and `{rand2}`.')
                    if(rand1 == 6 and rand2 == 6):
                        psum[turn] = 0;
                        pcsum = 0
                        await ctx.send(outp + f'\n{targets[turn].mention} rolled a double 6. Yikes, they lose all their points.')
                        break
                    if(rand1 == 6 or rand2 == 6):
                        pcsum = 0
                        await ctx.send(outp + f'\n{targets[turn].mention} rolled a 6. Turn is over, no points is given.')
                        break
                    pcsum += rand1 + rand2
                    await ctx.send(outp)
                psum[turn] += pcsum
                await ctx.send(f'\n{targets[turn].mention} ended this round with {psum[turn]} points.{printScore()}')
        
        if(await playGame() == 'quit'):
            await ctx.send('You have quit the game.')
            helper.log_event(f'{ctx.author}\'s greedypig game was quited.')
            return
        helper.log_event(f'ctx.author has finished their greedypig game.')
    
    @commands.command(name='tictactoe', help='Plays a tictactoe game! Code contributed by Rory.')
    async def tictactoe(self, ctx):
        async def drawBoard(board):
        # This function prints out the board that it was passed.

        # "board" is a list of 10 strings representing the board (ignore index 0)
            await ctx.send(str('```' + board[1] + '|' + board[2] + '|' + board[3]) + '\n-+-+-\n' + board[4] + '|' + board[5] + '|' + board[6] + '\n-+-+-\n' + board[7] + '|' + board[8] + '|' + board[9] + '```')

        async def inputPlayerLetter():
            # Lets the player type which letter they want to be.
            # Returns a list with the player's letter as the first item, and the computer's letter as the second.
            letter = ''
            while not (letter == 'X' or letter == 'O'):
                await ctx.send('Do you want to be X or O?')
                
                letter = str((await self.bot.wait_for('message', timeout=180.0, check=lambda msg: msg.author == ctx.author)).content).upper()

            # the first element in the list is the player's letter, the second is the computer's letter.
            if letter == 'X':
                return ['X', 'O']
            else:
                return ['O', 'X']

        def whoGoesFirst():
            # Randomly choose the player who goes first.
            if random.randint(0, 1) == 0:
                return 'computer'
            else:
                return 'player'

        def makeMove(board, letter, move):
            board[move] = letter

        def isWinner(bo, le):
            # Given a board and a player's letter, this function returns True if that player has won.
            # We use bo instead of board and le instead of letter so we don't have to type as much.
            return ((bo[7] == le and bo[8] == le and bo[9] == le) or # across the top
            (bo[4] == le and bo[5] == le and bo[6] == le) or # across the middle
            (bo[1] == le and bo[2] == le and bo[3] == le) or # across the bottom
            (bo[7] == le and bo[4] == le and bo[1] == le) or # down the left side
            (bo[8] == le and bo[5] == le and bo[2] == le) or # down the middle
            (bo[9] == le and bo[6] == le and bo[3] == le) or # down the right side
            (bo[7] == le and bo[5] == le and bo[3] == le) or # diagonal
            (bo[9] == le and bo[5] == le and bo[1] == le)) # diagonal

        def getBoardCopy(board):
            # Make a copy of the board list and return it.
            boardCopy = []
            for i in board:
                boardCopy.append(i)
            return boardCopy

        def isSpaceFree(board, move):
            # Return true if the passed move is free on the passed board.
            return board[move] == ' '

        async def getPlayerMove(board):
            # Let the player type in their move.
            move = ' '
            while move not in '1 2 3 4 5 6 7 8 9 quit'.split() or not isSpaceFree(board, int(move)):
                await ctx.send('What is your next move? (1-9, or quit)')
                move = str((await self.bot.wait_for('message', timeout=180.0, check=lambda msg: msg.author == ctx.author)).content).lower()
            if(move == 'quit'):
                return 'quit'
            return int(move)

        def chooseRandomMoveFromList(board, movesList):
            # Returns a valid move from the passed list on the passed board.
            # Returns None if there is no valid move.
            possibleMoves = []
            for i in movesList:
                if isSpaceFree(board, i):
                    possibleMoves.append(i)

            if len(possibleMoves) != 0:
                return random.choice(possibleMoves)
            else:
                return None

        def getComputerMove(board, computerLetter):
            # Given a board and the computer's letter, determine where to move and return that move.
            if computerLetter == 'X':
                playerLetter = 'O'
            else:
                playerLetter = 'X'

            # Here is our algorithm for our Tic Tac Toe AI:
            # First, check if we can win in the next move
            for i in range(1, 10):
                boardCopy = getBoardCopy(board)
                if isSpaceFree(boardCopy, i):
                    makeMove(boardCopy, computerLetter, i)
                    if isWinner(boardCopy, computerLetter):
                        return i

            # Check if the player could win on his next move, and block them.
            for i in range(1, 10):
                boardCopy = getBoardCopy(board)
                if isSpaceFree(boardCopy, i):
                    makeMove(boardCopy, playerLetter, i)
                    if isWinner(boardCopy, playerLetter):
                        return i

            # Try to take one of the corners, if they are free.
            move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
            if move != None:
                return move

            # Try to take the center, if it is free.
            if isSpaceFree(board, 5):
                return 5

            # Move on one of the sides.
            return chooseRandomMoveFromList(board, [2, 4, 6, 8])

        def isBoardFull(board):
            # Return True if every space on the board has been taken. Otherwise return False.
            for i in range(1, 10):
                if isSpaceFree(board, i):
                    return False
            return True

        await ctx.send('Welcome to Tic Tac Toe!\nCode contributed by Rory; modified for Discord by Justin')

        while True:
            # Reset the board
            theBoard = [' '] * 10
            playerLetter, computerLetter = await inputPlayerLetter()
            turn = whoGoesFirst()
            await ctx.send(str('The ' + turn + ' will go first.'))
            gameIsPlaying = True

            while gameIsPlaying:
                if turn == 'player':
                    # Player's turn.
                    await drawBoard(theBoard)
                    move = await getPlayerMove(theBoard)
                    if(move == 'quit'):
                        await ctx.send('You have quit the game.')
                        helper.log_event(f'{ctx.author} has quit their tictactoe game.')
                    makeMove(theBoard, playerLetter, move)

                    if isWinner(theBoard, playerLetter):
                        await drawBoard(theBoard)
                        await ctx.send('Hooray! You have won the game!')
                        gameIsPlaying = False
                    else:
                        if isBoardFull(theBoard):
                            drawBoard(theBoard)
                            await ctx.send('The game is a tie!')
                            print('The game is a tie!')
                            break
                        else:
                            turn = 'computer'

                else:
                    # Computer's turn.
                    move = getComputerMove(theBoard, computerLetter)
                    makeMove(theBoard, computerLetter, move)

                    if isWinner(theBoard, computerLetter):
                        await drawBoard(theBoard)
                        await ctx.send('The computer has beaten you! You lose.')
                        gameIsPlaying = False
                    else:
                        if isBoardFull(theBoard):
                            await drawBoard(theBoard)
                            await ctx.send('The game is a tie!')
                            break
                        else:
                            turn = 'player'
            await ctx.send('Do you want to play again? (yes or no)')
            if not str((await self.bot.wait_for('message', timeout=180.0, check=lambda msg: msg.author == ctx.author)).content).lower().startswith('y'):
                await ctx.send('Ok cya loser.')
                break
    @commands.command(name='othello', help='Plays a othello game! Code contributed by Rory.')
    async def othello(self, ctx):
        helper.log_event(str(ctx.author) + ' started a game of othello.')
        async def vpcOthello():
            # Othello
            WIDTH = 8  # Board is 8 spaces wide
            HEIGHT = 8 # Board is 8 spaces tall
            async def drawBoard(board):
                # This function prints the board that it was passed. Returns None.
                DBstr = '```'
                DBstr = DBstr + '  12345678\n +--------+\n'
                for y in range(HEIGHT):
                    DBstr = DBstr + str(y+1) + '|'
                    for x in range(WIDTH):
                        DBstr = DBstr + str(board[x][y])
                    DBstr = DBstr + '|' + str(y+1) + '\n'
                DBstr = DBstr + ' +--------+\n  12345678```'
                await ctx.send(DBstr)


            def getNewBoard():
                # Creates a brand-new, blank board data structure.
                board = []
                for i in range(WIDTH):
                    board.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
                return board

            def isValidMove(board, tile, xstart, ystart):
                # Returns False if the player's move on space xstart, ystart is invalid.
                # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
                if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
                    return False

                if tile == 'X':
                    otherTile = 'O'
                else:
                    otherTile = 'X'

                tilesToFlip = []
                for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
                    x, y = xstart, ystart
                    x += xdirection # First step in the x direction
                    y += ydirection # First step in the y direction
                    while isOnBoard(x, y) and board[x][y] == otherTile:
                        # Keep moving in this x & y direction.
                        x += xdirection
                        y += ydirection
                        if isOnBoard(x, y) and board[x][y] == tile:
                            # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                            while True:
                                x -= xdirection
                                y -= ydirection
                                if x == xstart and y == ystart:
                                    break
                                tilesToFlip.append([x, y])

                if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
                    return False
                return tilesToFlip

            def isOnBoard(x, y):
                # Returns True if the coordinates are located on the board.
                return x >= 0 and x <= WIDTH - 1 and y >= 0 and y <= HEIGHT - 1

            def getBoardWithValidMoves(board, tile):
                # Returns a new board with periods marking the valid moves the player can make.
                boardCopy = getBoardCopy(board)

                for x, y in getValidMoves(boardCopy, tile):
                    boardCopy[x][y] = '.'
                return boardCopy

            def getValidMoves(board, tile):
                # Returns a list of [x,y] lists of valid moves for the given player on the given board.
                validMoves = []
                for x in range(WIDTH):
                    for y in range(HEIGHT):
                        if isValidMove(board, tile, x, y) != False:
                            validMoves.append([x, y])
                return validMoves

            def getScoreOfBoard(board):
                # Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'.
                xscore = 0
                oscore = 0
                for x in range(WIDTH):
                    for y in range(HEIGHT):
                        if board[x][y] == 'X':
                            xscore += 1
                        if board[x][y] == 'O':
                            oscore += 1
                return {'X':xscore, 'O':oscore}

            async def enterPlayerTile():
                # Lets the player type which tile they want to be.
                # Returns a list with the player's tile as the first item and the computer's tile as the second.
                tile = ''
                while not (tile == 'X' or tile == 'O' or tile == 'QUIT'):
                    await ctx.send('Do you want to be X or O?')
                    tile = (str((await self.bot.wait_for('message', timeout=180.0, check=lambda msg: msg.author == ctx.author)).content)).upper() 

                # The first element in the list is the player's tile, and the second is the computer's tile.
                if tile == 'QUIT':
                    return ['quit', 'quit']
                elif tile == 'X':
                    return ['X', 'O']
                else:
                    return ['O', 'X']

            def whoGoesFirst():
                # Randomly choose who goes first.
                if random.randint(0, 1) == 0:
                    return 'computer'
                else:
                    return 'player'

            def makeMove(board, tile, xstart, ystart):
                # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
                # Returns False if this is an invalid move; True if it is valid.
                tilesToFlip = isValidMove(board, tile, xstart, ystart)

                if tilesToFlip == False:
                    return False

                board[xstart][ystart] = tile
                for x, y in tilesToFlip:
                    board[x][y] = tile
                return True

            def getBoardCopy(board):
                # Make a duplicate of the board list and return it.
                boardCopy = getNewBoard()

                for x in range(WIDTH):
                    for y in range(HEIGHT):
                        boardCopy[x][y] = board[x][y]

                return boardCopy

            def isOnCorner(x, y):
                # Returns True if the position is in one of the four corners.
                return (x == 0 or x == WIDTH - 1) and (y == 0 or y == HEIGHT - 1)

            async def getPlayerMove(board, playerTile):
                # Let the player enter their move.
                # Returns the move as [x, y] (or returns the strings 'hints' or 'quit').
                DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
                while True:
                    await ctx.send('Enter your move, "quit" to end the game, or "hints" to toggle hints.')
                    move = (str((await self.bot.wait_for('message', timeout=180.0, check=lambda msg: msg.author == ctx.author)).content)).lower()
                    if move == 'quit' or move == 'hints':
                        return move

                    if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
                        x = int(move[0]) - 1
                        y = int(move[1]) - 1
                        if isValidMove(board, playerTile, x, y) == False:
                            await ctx.send('That is not a valid move! See \"hints\" for a valid moves')
                            continue
                        else:
                            break
                    else:
                        await ctx.send('That is not a valid move. Enter the column (1-8) and then the row (1-8).\nFor example, 81 will move on the top-right corner.')

                return [x, y]

            def getComputerMove(board, computerTile):
                # Given a board and the computer's tile, determine where to
                # move and return that move as a [x, y] list.
                possibleMoves = getValidMoves(board, computerTile)
                random.shuffle(possibleMoves) # randomize the order of the moves

                # Always go for a corner if available.
                for x, y in possibleMoves:
                    if isOnCorner(x, y):
                        return [x, y]

                # Find the highest-scoring move possible.
                bestScore = -1
                for x, y in possibleMoves:
                    boardCopy = getBoardCopy(board)
                    makeMove(boardCopy, computerTile, x, y)
                    score = getScoreOfBoard(boardCopy)[computerTile]
                    if score > bestScore:
                        bestMove = [x, y]
                        bestScore = score
                return bestMove

            async def printScore(board, playerTile, computerTile):
                scores = getScoreOfBoard(board)
                await ctx.send('You: ' + str(scores[playerTile]) + ' points. Computer: ' + str(scores[computerTile]) + ' points.')

            async def playGame(playerTile, computerTile):
                showHints = False
                turn = whoGoesFirst()
                await ctx.send('The ' + turn + ' will go first.')

                # Clear the board and place starting pieces.
                board = getNewBoard()
                board[3][3] = 'X'
                board[3][4] = 'O'
                board[4][3] = 'O'
                board[4][4] = 'X'

                while True:
                    playerValidMoves = getValidMoves(board, playerTile)
                    computerValidMoves = getValidMoves(board, computerTile)

                    if playerValidMoves == [] and computerValidMoves == []:
                        return board # No one can move, so end the game.

                    elif turn == 'player': # Player's turn
                        if playerValidMoves != []:
                            if showHints:
                                validMovesBoard = getBoardWithValidMoves(board, playerTile)
                                await drawBoard(validMovesBoard)
                            else:
                                await drawBoard(board)
                            await printScore(board, playerTile, computerTile)

                            move = await getPlayerMove(board, playerTile)
                            if move == 'quit':
                                await ctx.send('Thanks for playing!')
                                return 'quit' # Terminate the program.
                            elif move == 'hints':
                                showHints = not showHints
                                continue
                            else:
                                makeMove(board, playerTile, move[0], move[1])
                        turn = 'computer'

                    elif turn == 'computer': # Computer's turn
                        if computerValidMoves != []:
                            await drawBoard(board)
                            await printScore(board, playerTile, computerTile)
                            move = getComputerMove(board, computerTile)
                            makeMove(board, computerTile, move[0], move[1])
                        turn = 'player'



            await ctx.send('O T H E L L O\n**Code by Rory**')

            playerTile, computerTile = await enterPlayerTile()
            
            if(playerTile == 'quit' and computerTile == 'quit'):
                await ctx.send('You have ended your game of othello.')
                helper.log_event(f'{ctx.author} has ended their game of othello.')
                return
            while True:
                finalBoard = await playGame(playerTile, computerTile)
                if finalBoard == 'quit':
                    await ctx.send('You have ended your game of othello.')
                    helper.log_event(str(ctx.author) + ' has ended their game of othello.')
                    return
                
                # Display the final score.
                await drawBoard(finalBoard)
                scores = getScoreOfBoard(finalBoard)
                await ctx.send('X scored ' + scores['X'] + ' points. O scored ' + scores['O'] + ' points.')
                if scores[playerTile] > scores[computerTile]:
                    await ctx.send('You beat the computer by ' + scores[playerTile] - scores[computerTile] + ' points! Congratulations!')
                elif scores[playerTile] < scores[computerTile]:
                    await ctx.send('You lost. The computer beat you by ' + scores[computerTile] - scores[playerTile])
                else:
                    await ctx.send('The game was a tie!')

                await ctx.send('Do you want to play again? (yes or no)')
                if not (str((await self.bot.wait_for('message', timeout=180.0, check=lambda msg: msg.author == ctx.author)).content)).lower().startswith('y'):
                    break

        async def pvsOthello():
            # PvP Othello
            WIDTH = 8  # Board is 8 spaces wide
            HEIGHT = 8 # Board is 8 spaces tall
            async def drawBoard(board):
                # This function prints the board that it was passed. Returns None.
                DBstr = '```'
                DBstr = DBstr + '  12345678\n +--------+\n'
                for y in range(HEIGHT):
                    DBstr = DBstr + str(y+1) + '|'
                    for x in range(WIDTH):
                        DBstr = DBstr + str(board[x][y])
                    DBstr = DBstr + '|' + str(y+1) + '\n'
                DBstr = DBstr + ' +--------+\n  12345678```'
                await ctx.send(DBstr)

            def getNewBoard():
                # Creates a brand-new, blank board data structure.
                board = []
                for i in range(WIDTH):
                    board.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
                return board

            def isValidMove(board, tile, xstart, ystart):
                # Returns False if the player's move on space xstart, ystart is invalid.
                # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
                if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
                    return False

                if tile == 'X':
                    otherTile = 'O'
                else:
                    otherTile = 'X'

                tilesToFlip = []
                for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
                    x, y = xstart, ystart
                    x += xdirection # First step in the x direction
                    y += ydirection # First step in the y direction
                    while isOnBoard(x, y) and board[x][y] == otherTile:
                        # Keep moving in this x & y direction.
                        x += xdirection
                        y += ydirection
                        if isOnBoard(x, y) and board[x][y] == tile:
                            # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                            while True:
                                x -= xdirection
                                y -= ydirection
                                if x == xstart and y == ystart:
                                    break
                                tilesToFlip.append([x, y])

                if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
                    return False
                return tilesToFlip

            def isOnBoard(x, y):
                # Returns True if the coordinates are located on the board.
                return x >= 0 and x <= WIDTH - 1 and y >= 0 and y <= HEIGHT - 1

            def getBoardWithValidMoves(board, tile):
                # Returns a new board with periods marking the valid moves the player can make.
                boardCopy = getBoardCopy(board)

                for x, y in getValidMoves(boardCopy, tile):
                    boardCopy[x][y] = '.'
                return boardCopy

            def getValidMoves(board, tile):
                # Returns a list of [x,y] lists of valid moves for the given player on the given board.
                validMoves = []
                for x in range(WIDTH):
                    for y in range(HEIGHT):
                        if isValidMove(board, tile, x, y) != False:
                            validMoves.append([x, y])
                return validMoves

            def getScoreOfBoard(board):
                # Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'.
                xscore = 0
                oscore = 0
                for x in range(WIDTH):
                    for y in range(HEIGHT):
                        if board[x][y] == 'X':
                            xscore += 1
                        if board[x][y] == 'O':
                            oscore += 1
                return {'X':xscore, 'O':oscore}

            async def enterPlayerTile():
                # Lets the player type which tile they want to be.
                # Returns a list with the player's tile as the first item and the computer's tile as the second.
                tile = ''
                while not (tile == 'X' or tile == 'O' or tile == 'QUIT'):
                    await ctx.send('Does player 1 want to be X or O?')
                    tile = (str((await self.bot.wait_for('message', timeout=180.0, check=lambda msg: msg.author == ctx.author)).content)).upper()

                # The first element in the list is the player's tile, and the second is the computer's tile.
                if tile == 'QUIT':
                    return ['quit', 'quit']
                elif tile == 'X':
                    return ['X', 'O']
                else:
                    return ['O', 'X']

            def whoGoesFirst():
                # Randomly choose who goes first.
                if random.randint(0, 1) == 0:
                    return 'player1'
                else:
                    return 'player2'

            def makeMove(board, tile, xstart, ystart):
                # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
                # Returns False if this is an invalid move; True if it is valid.
                tilesToFlip = isValidMove(board, tile, xstart, ystart)

                if tilesToFlip == False:
                    return False

                board[xstart][ystart] = tile
                for x, y in tilesToFlip:
                    board[x][y] = tile
                return True

            def getBoardCopy(board):
                # Make a duplicate of the board list and return it.
                boardCopy = getNewBoard()

                for x in range(WIDTH):
                    for y in range(HEIGHT):
                        boardCopy[x][y] = board[x][y]

                return boardCopy

            def isOnCorner(x, y):
                # Returns True if the position is in one of the four corners.
                return (x == 0 or x == WIDTH - 1) and (y == 0 or y == HEIGHT - 1)

            async def getPlayer1Move(board, player1Tile):
                # Let the player enter their move.
                # Returns the move as [x, y] (or returns the strings 'hints' or 'quit').
                DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
                while True:
                    await ctx.send('Player 1 enter your move, "quit" to end the game, or "hints" to toggle hints.')
                    move = str((await self.bot.wait_for('message', timeout=180.0, check=lambda msg: msg.author == ctx.author)).content).lower()
                    if move == 'quit' or move == 'hints':
                        return move

                    if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
                        x = int(move[0]) - 1
                        y = int(move[1]) - 1
                        if isValidMove(board, player1Tile, x, y) == False:
                            await ctx.send('That is not a valid move. Press \"hints\" for valid moves. If you have hints on, look for the dots on the board for valid moves.')
                            continue
                        else:
                            break
                    else:
                        await ctx.send('That is not a valid move. Enter the column (1-8) and then the row (1-8).\nFor example, 81 will move on the top-right corner.')

                return [x, y]

            async def getPlayer2Move(board, player2Tile):
                # Let the player enter their move.
                # Returns the move as [x, y] (or returns the strings 'hints' or 'quit').
                DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
                while True:
                    await ctx.send('Player 2 enter your move, "quit" to end the game, or "hints" to toggle hints.')
                    move = str((await self.bot.wait_for('message', timeout=180.0, check=lambda msg: msg.author == ctx.author)).content).lower()
                    if move == 'quit' or move == 'hints':
                        return move

                    if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
                        x = int(move[0]) - 1
                        y = int(move[1]) - 1
                        if isValidMove(board, player2Tile, x, y) == False:
                            await ctx.send('That is not a valid move. Press \"hints\" for valid moves. If you have hints on, look for the dots on the board for valid moves.')
                            continue
                        else:
                            break
                    else:
                        await ctx.send('That is not a valid move. Enter the column (1-8) and then the row (1-8).\nFor example, 81 will move on the top-right corner.')

                return [x, y]

            async def printScore(board, player1Tile, player2Tile):
                scores = getScoreOfBoard(board)
                await ctx.send('Player 1: ' + str(scores[player1Tile]) + ' points. Player 2: ' + str(scores[player2Tile]) + ' points.')

            async def playGame(player1Tile, player2Tile):
                showHints = False
                turn = whoGoesFirst()
                await ctx.send(str(turn) + ' will go first.')

                # Clear the board and place starting pieces.
                board = getNewBoard()
                board[3][3] = 'X'
                board[3][4] = 'O'
                board[4][3] = 'O'
                board[4][4] = 'X'

                while True:
                    player1ValidMoves = getValidMoves(board, player1Tile)
                    player2ValidMoves = getValidMoves(board, player2Tile)

                    if player1ValidMoves == [] and player2ValidMoves == []:
                        return board # No one can move, so end the game.

                    elif turn == 'player1': # Player's turn
                        if player1ValidMoves != []:
                            if showHints:
                                validMovesBoard = getBoardWithValidMoves(board, player1Tile)
                                await drawBoard(validMovesBoard)
                            else:
                                await drawBoard(board)
                            await printScore(board, player1Tile, player2Tile)

                            move = await getPlayer1Move(board, player1Tile)
                            if move == 'quit':
                                await ctx.send('Thanks for playing!')
                                return 'quit' # Terminate the program.
                            elif move == 'hints':
                                showHints = not showHints
                                continue
                            else:
                                makeMove(board, player1Tile, move[0], move[1])
                        turn = 'player2'

                    elif turn == 'player2': # Player's turn
                        if player2ValidMoves != []:
                            if showHints:
                                validMovesBoard = getBoardWithValidMoves(board, player2Tile)
                                await drawBoard(validMovesBoard)
                            else:
                                await drawBoard(board)
                            await printScore(board, player1Tile, player2Tile)

                            move = await getPlayer2Move(board, player2Tile)
                            if move == 'quit':
                                await ctx.send('Thanks for playing!')
                                return 'quit' # Terminate the program.
                            elif move == 'hints':
                                showHints = not showHints
                                continue
                            else:
                                makeMove(board, player2Tile, move[0], move[1])
                        turn = 'player1'



            await ctx.send('O T H E L L O\n**Code contributed by Rory**\n')

            player1Tile, player2Tile = await enterPlayerTile()
            
            if(playerTile == 'quit' and computerTile == 'quit'):
                await ctx.send('You have ended your game of othello.')
                helper.log_event(f'{ctx.author} has ended their game of othello.')
                return

            while True:
                finalBoard = await playGame(player1Tile, player2Tile)
                if finalBoard == 'quit':
                    helper.log_event(str(ctx.author) + ' has ended their game of othello.')
                    return

                # Display the final score.
                await drawBoard(finalBoard)
                scores = getScoreOfBoard(finalBoard)
                await ctx.send('X scored ' + str(scores['X']) + ' points. O scored ' + str(scores['O']) + ' points.')
                if scores[player1Tile] > scores[player2Tile]:
                    await ctx.send('Player 1 beat Player 2 ' + str(scores[player1Tile] - scores[player2Tile]) + ' points! Congratulations!')
                elif scores[player1Tile] < scores[player2Tile]:
                    await ctx.send('Player 2 beat Player 1 ' + str(scores[player2Tile] - scores[player1Tile]) + ' points! Congratulations!')
                else:
                    await ctx.send('The game was a tie!')

                await ctx.send('Do you want to play again? (yes or no)')
                if not str((await self.bot.wait_for('message', timeout=180.0, check=lambda msg: msg.author == ctx.author)).content).lower().startswith('y'):
                    break
        
        async def pvpOthello():
            while(True):
                await ctx.send('Ping another user!')
                ping = str((await self.bot.wait_for('message', timeout=180.0, check=lambda msg: msg.author == ctx.author)).content) 
                target = self.bot.get_user(int(get_id(ping)))
                if target != None:
                    break
            player1 = None
            player2 = None
            # PvP Othello
            WIDTH = 8  # Board is 8 spaces wide
            HEIGHT = 8 # Board is 8 spaces tall
            async def drawBoard(board):
                # This function prints the board that it was passed. Returns None.
                DBstr = '```'
                DBstr = DBstr + '  12345678\n +--------+\n'
                for y in range(HEIGHT):
                    DBstr = DBstr + str(y+1) + '|'
                    for x in range(WIDTH):
                        DBstr = DBstr + str(board[x][y])
                    DBstr = DBstr + '|' + str(y+1) + '\n'
                DBstr = DBstr + ' +--------+\n  12345678```'
                await ctx.send(DBstr)

            def getNewBoard():
                # Creates a brand-new, blank board data structure.
                board = []
                for i in range(WIDTH):
                    board.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
                return board

            def isValidMove(board, tile, xstart, ystart):
                # Returns False if the player's move on space xstart, ystart is invalid.
                # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
                if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
                    return False

                if tile == 'X':
                    otherTile = 'O'
                else:
                    otherTile = 'X'

                tilesToFlip = []
                for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
                    x, y = xstart, ystart
                    x += xdirection # First step in the x direction
                    y += ydirection # First step in the y direction
                    while isOnBoard(x, y) and board[x][y] == otherTile:
                        # Keep moving in this x & y direction.
                        x += xdirection
                        y += ydirection
                        if isOnBoard(x, y) and board[x][y] == tile:
                            # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                            while True:
                                x -= xdirection
                                y -= ydirection
                                if x == xstart and y == ystart:
                                    break
                                tilesToFlip.append([x, y])

                if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
                    return False
                return tilesToFlip

            def isOnBoard(x, y):
                # Returns True if the coordinates are located on the board.
                return x >= 0 and x <= WIDTH - 1 and y >= 0 and y <= HEIGHT - 1

            def getBoardWithValidMoves(board, tile):
                # Returns a new board with periods marking the valid moves the player can make.
                boardCopy = getBoardCopy(board)

                for x, y in getValidMoves(boardCopy, tile):
                    boardCopy[x][y] = '.'
                return boardCopy

            def getValidMoves(board, tile):
                # Returns a list of [x,y] lists of valid moves for the given player on the given board.
                validMoves = []
                for x in range(WIDTH):
                    for y in range(HEIGHT):
                        if isValidMove(board, tile, x, y) != False:
                            validMoves.append([x, y])
                return validMoves

            def getScoreOfBoard(board):
                # Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'.
                xscore = 0
                oscore = 0
                for x in range(WIDTH):
                    for y in range(HEIGHT):
                        if board[x][y] == 'X':
                            xscore += 1
                        if board[x][y] == 'O':
                            oscore += 1
                return {'X':xscore, 'O':oscore}

            async def enterPlayerTile():
                # Lets the player type which tile they want to be.
                # Returns a list with the player's tile as the first item and the computer's tile as the second.
                tile = ''
                while not (tile == 'X' or tile == 'O'or tile == 'QUIT'):
                    await ctx.send('Does player 1 want to be X or O?')
                    tile = (str((await self.bot.wait_for('message', timeout=180.0, check=lambda msg: msg.author == ctx.author)).content)).upper()

                # The first element in the list is the player's tile, and the second is the computer's tile.
                if tile == 'QUIT':
                    return ['quit', 'quit']
                elif tile == 'X':
                    return ['X', 'O']
                else:
                    return ['O', 'X']

            def whoGoesFirst():
                # Randomly choose who goes first. haha
                nonlocal player1
                nonlocal player2
                if random.randint(0, 1) == 0:
                    player1 = ctx.author
                    player2 = target
                    return 'player1'
                else:
                    player1 = target
                    player2 = ctx.author
                    return 'player2'

            def makeMove(board, tile, xstart, ystart):
                # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
                # Returns False if this is an invalid move; True if it is valid.
                tilesToFlip = isValidMove(board, tile, xstart, ystart)

                if tilesToFlip == False:
                    return False

                board[xstart][ystart] = tile
                for x, y in tilesToFlip:
                    board[x][y] = tile
                return True

            def getBoardCopy(board):
                # Make a duplicate of the board list and return it.
                boardCopy = getNewBoard()

                for x in range(WIDTH):
                    for y in range(HEIGHT):
                        boardCopy[x][y] = board[x][y]

                return boardCopy

            def isOnCorner(x, y):
                # Returns True if the position is in one of the four corners.
                return (x == 0 or x == WIDTH - 1) and (y == 0 or y == HEIGHT - 1)

            async def getPlayer1Move(board, player1Tile):
                # Let the player enter their move.
                # Returns the move as [x, y] (or returns the strings 'hints' or 'quit').
                DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
                while True:
                    await ctx.send('Player 1 enter your move, "quit" to end the game, or "hints" to toggle hints.')
                    move = str((await self.bot.wait_for('message', timeout=180.0, check=lambda msg: msg.author == player1)).content).lower()
                    if move == 'quit' or move == 'hints':
                        return move

                    if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
                        x = int(move[0]) - 1
                        y = int(move[1]) - 1
                        if isValidMove(board, player1Tile, x, y) == False:
                            await ctx.send('That is not a valid move. Press \"hints\" for valid moves. If you have hints on, look for the dots on the board for valid moves.')
                            continue
                        else:
                            break
                    else:
                        await ctx.send('That is not a valid move. Enter the column (1-8) and then the row (1-8).\nFor example, 81 will move on the top-right corner.')

                return [x, y]

            async def getPlayer2Move(board, player2Tile):
                # Let the player enter their move.
                # Returns the move as [x, y] (or returns the strings 'hints' or 'quit').
                DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
                while True:
                    await ctx.send('Player 2 enter your move, "quit" to end the game, or "hints" to toggle hints.')
                    move = str((await self.bot.wait_for('message', timeout=180.0, check=lambda msg: msg.author == player2)).content).lower()
                    if move == 'quit' or move == 'hints':
                        return move

                    if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
                        x = int(move[0]) - 1
                        y = int(move[1]) - 1
                        if isValidMove(board, player2Tile, x, y) == False:
                            await ctx.send('That is not a valid move. Press \"hints\" for valid moves. If you have hints on, look for the dots on the board for valid moves.')
                            continue
                        else:
                            break
                    else:
                        await ctx.send('That is not a valid move. Enter the column (1-8) and then the row (1-8).\nFor example, 81 will move on the top-right corner.')

                return [x, y]

            async def printScore(board, player1Tile, player2Tile):
                scores = getScoreOfBoard(board)
                await ctx.send('Player 1: ' + str(scores[player1Tile]) + ' points. Player 2: ' + str(scores[player2Tile]) + ' points.')

            async def playGame(player1Tile, player2Tile):
                showHints = False
                turn = whoGoesFirst()
                print(player1, player2)
                await ctx.send(str(turn) + ' will go first.')

                # Clear the board and place starting pieces.
                board = getNewBoard()
                board[3][3] = 'X'
                board[3][4] = 'O'
                board[4][3] = 'O'
                board[4][4] = 'X'

                while True:
                    player1ValidMoves = getValidMoves(board, player1Tile)
                    player2ValidMoves = getValidMoves(board, player2Tile)

                    if player1ValidMoves == [] and player2ValidMoves == []:
                        return board # No one can move, so end the game.

                    elif turn == 'player1': # Player's turn
                        if player1ValidMoves != []:
                            if showHints:
                                validMovesBoard = getBoardWithValidMoves(board, player1Tile)
                                await drawBoard(validMovesBoard)
                            else:
                                await drawBoard(board)
                            await printScore(board, player1Tile, player2Tile)

                            move = await getPlayer1Move(board, player1Tile)
                            if move == 'quit':
                                await ctx.send('Thanks for playing!')
                                return 'quit' # Terminate the program.
                            elif move == 'hints':
                                showHints = not showHints
                                continue
                            else:
                                makeMove(board, player1Tile, move[0], move[1])
                        turn = 'player2'

                    elif turn == 'player2': # Player's turn
                        if player2ValidMoves != []:
                            if showHints:
                                validMovesBoard = getBoardWithValidMoves(board, player2Tile)
                                await drawBoard(validMovesBoard)
                            else:
                                await drawBoard(board)
                            await printScore(board, player1Tile, player2Tile)

                            move = await getPlayer2Move(board, player2Tile)
                            if move == 'quit':
                                await ctx.send('Thanks for playing!')
                                return 'quit' # Terminate the program.
                            elif move == 'hints':
                                showHints = not showHints
                                continue
                            else:
                                makeMove(board, player2Tile, move[0], move[1])
                        turn = 'player1'



            await ctx.send('O T H E L L O\n**Code contributed by Rory**\n')

            player1Tile, player2Tile = await enterPlayerTile()
            
            if(playerTile == 'quit' and computerTile == 'quit'):
                await ctx.send('You have ended your game of othello.')
                helper.log_event(f'{ctx.author} has ended their game of othello.')
                return

            while True:
                finalBoard = await playGame(player1Tile, player2Tile)
                if finalBoard == 'quit':
                    helper.log_event(str(ctx.author) + ' has ended their game of othello.')
                    return

                # Display the final score.
                await drawBoard(finalBoard)
                scores = getScoreOfBoard(finalBoard)
                await ctx.send('X scored ' + str(scores['X']) + ' points. O scored ' + str(scores['O']) + ' points.')
                if scores[player1Tile] > scores[player2Tile]:
                    await ctx.send('Player 1 beat Player 2 ' + str(scores[player1Tile] - scores[player2Tile]) + ' points! Congratulations!')
                elif scores[player1Tile] < scores[player2Tile]:
                    await ctx.send('Player 2 beat Player 1 ' + str(scores[player2Tile] - scores[player1Tile]) + ' points! Congratulations!')
                else:
                    await ctx.send('The game was a tie!')

                await ctx.send('Do the either of you want to play again? (yes or no)')
                if not str(await self.bot.wait_for('message', timeout=180.0, check=lambda msg: msg.author == player1 or msg.author == player2)).content.lower().startswith('y'):
                    break
        await ctx.send('Choose an option:```\nA: Vs Computer\nB: Vs Another discord user\nC: Vs Yourself (someone else using the same computer)```')
        while(True):
            choice = str((await self.bot.wait_for('message', timeout=180.0, check = lambda msg: msg.author == ctx.author)).content).upper()
            if(choice == 'A'):
                await vpcOthello()
                break
            elif(choice == 'B'):
                await pvpOthello()
                break
            elif(choice == 'C'):
                await pvsOthello()
                break
            elif(choice == 'QUIT'):
                await ctx.send('You have quit your Othello game.')
                helper.log_event(f'{ctx.author} has ended their Othello game.')
                return 'quit'
            else:
                await ctx.send('Please choose between option `A`, `B`, or `C`')
        helper.log_event(str(ctx.author) + ' has finished their game of othello.')
    
    @hangman.error
    @greedypigs.error
    @othello.error
    @tictactoe.error
    async def err_handling(ctx, error):
        error = getattr(error, "original", error)
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            log_event('Unsucessful. Missing arg.')
            await ctx.send('You need an argument here! Try obama help <command>')
        elif(isinstance(error, asyncio.TimeoutError)):
            log_event(str(ctx.author) + "'s game has timed out!")
            await ctx.send('Wow rude. I sat here waiting for you for so long... (Session Over)')
        elif(isinstance(error, discord.ext.commands.errors.CommandOnCooldown)):
            if(ctx.author.id not in blacklist):
                log_event(str(ctx.author))
                await ctx.send(str(error))
            
        else:
            await ctx.send('An exception occured during your request: `' + str(error) + '`')
        print(traceback.format_exc())
        log_event(str(ctx.author) + ': ' + str(error))

def setup(bot):
    bot.add_cog(games(bot))