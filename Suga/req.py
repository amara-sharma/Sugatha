import random
def fun():
    Quotes=["Service to others is the rent you pay for your room here on earth.","If there be any truer measure of a man than by what he does, it must be by what he gives.","If you knew what I know about the power of giving, you would not let a single meal pass without sharing it in some way.","We make a living by what we get, but we make a life by what we give.","Caring has the gift of making the ordinary special.","God does watch over us and does notice us, but it is usually through someone else that he meets our needs.","Nature does not give to those who will not spend…","Getters don’t get — givers get.","To give requires good sense.","At the end of life we will not be judged by how many diplomas we have received, how much money we have made, how many great things we have done.We will be judged by I was hungry, and you gave me something to eat, I was naked and you clothed me. I was homeless, and you took me in.","Only a life lived for others is a life worthwhile.","The best way to find yourself is to lose yourself in the service of others.","He who wishes to secure the good of others, has already secured his own.","Love cannot remain by itself – it has no meaning. Love has to be put into action and that action is service.","No act of kindness, no matter how small, is ever wasted.","Find out how much God has given you and from it take what you need; the remainder is needed by others."]
    Authors=["―Mohammed Ali","―Robert South","―Buddha","―Winston Churchill","―George R. Bach","―Spencer W. Kimball","―R.J. Baughan","―Eugene Benge","―Ovid","―Mother Teresa",
            "―Albert Einstein","―Mahatma Gandhi","―Confucius","―Mother Teresa","―Aesop","―Saint Augustine"]


    print(len(Quotes),len(Authors))
    x=random.choice(Quotes)
    print(x)
    y=Quotes.index(x)
    z=Authors[y]
    print(x)
    print(z)
    return x,z
