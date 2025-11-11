##---------------------------------------------------------------------------##
##
## pyChing -- a Python program to cast and interpret I Ching hexagrams
##
## Copyright (C) 1999-2006 Stephen M. Gava
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be of some
## interest to somebody, but WITHOUT ANY WARRANTY; without even the 
## implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
## See the GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING or COPYING.txt. If not, 
##  write to the Free Software Foundation, Inc.,## 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
## The license can also be found at the GNU/FSF website: http://www.gnu.org
##
## Stephen M. Gava
## <elguavas@users.sourceforge.net>
## http://pyching.sourgeforge.net
##
##---------------------------------------------------------------------------##
""""
data return routines for pyching.
each of the numbered functions below returns the information text data for one
hexagram, after converting it to an html string
"""

from typing import Any

def BuildHtml(dict: dict[Any, Any]) -> str:
    """
    build an html hexagram info string from the passed in dict
    """
    #put the <p>'s between the text paragraphs
    textList=dict['text'].splitlines(1)
    for i in range(0,len(textList)):
        #print textList[i].strip()
        if textList[i].strip()=='':
            textList[i]="<p>"                
    textHtmlStr='\n'.join(textList)
    htmlStr=(
            """<html><body><p><h2><img SRC=%s"""%(dict['imgSrc'])+
            """> %s</h2><p>"""%(dict['title'])+
            """%s<p>"""%(textHtmlStr)+
            """<b>The bottom line</b>, as %s<p>"""%(dict[1])+
            """<b>The second line</b>, as %s<p>"""%(dict[2])+
            """<b>The third line</b>, as %s<p>"""%(dict[3])+
            """<b>The fourth line</b>, as %s<p>"""%(dict[4])+
            """<b>The fifth line</b>, as %s<p>"""%(dict[5])+
            """<b>The topmost line</b>, as %s<p>"""%(dict[6])+
            """</body></html>"""
            )
    return htmlStr


def in1data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id1data()",
                'title':""" 1. Tch'ien / The Creative""", 
                'text':"""
Heaven, in its motion, gives the idea of strength. The superior person, in accordance with this, will nerve their being to ceaseless activity.

Tch'ien represents what is great and originating, penetrating, advantageous, correct and firm.
""",
                1:"""nine: we see the dragon lying hidden in the deep. It is not the time for active doing.""",
                2:"""nine: we see the dragon appearing in the field. It will be advantageous to meet with the great person.""",
                3:"""nine: we see the superior person active and vigilant all the day, and in the evening still careful and apprehensive. The position is dangerous, but there will be no mistake. """,
                4:"""nine: we see the dragon looking as if they were leaping up, but still in the deep. There will be no mistake. """,
                5:"""nine: we see the dragon on the wing in the sky. It will be advantageous to meet with the great person. """,
                6:"""nine: we see the dragon exceeding the proper limits. There will be occasion for repentance."""
})
def in2data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id2data()",
                'title':""" 2. Koun / The Receptive""", 
                'text':"""
The capacity and sustaining power of the earth is what is denoted by Koun. The superior person, in accordance with this, supports people and things with their great virtue.

Koun represents what is great and originating, penetrating, advantageous, correct and having the firmness of a mare. When the superior person here denoted has to make any movement, if they take the initiative, they will go astray ; if they follow, they will find their proper lord. The advantage will be seen in their making friends in the south-west, and losing friends in the north-east. If they rest in correctness and firmness, there will be good fortune.
""",
                1:"""six: we see its subject treading on hoarfrost. The strong ice will come by and by.""",
                2:"""six: shows the attribute of being straight, square, and great. Its operation, without repeated efforts, will be in every respect advantageous.""",
                3:"""six: shows its subject keeping their excellence under restraint, but firmly maintaining it. If they should have occasion to engage in the king's service, though they will not claim the success for themselves, they will bring affairs to a good outcome. """,
                4:"""six: shows the symbol of a sack tied up. There will be no ground for blame or for praise. """,
                5:"""six: shows the yellow lower garment. There will be great good fortune. """,
                6:"""six: shows dragons fighting in the wild. Their blood is purple and yellow."""
})

def in3data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id3data()",
                'title':""" 3. T'oun / Difficult Beginnings""", 
                'text':"""
The trigram representing clouds and that representing thunder form T'oun. The superior person, in accordance with this, adjusts their measures of government as in sorting the threads of the warp and weft.

T'oun indicates that there can be great progress and success, and the advantage will come from being correct and firm. But any movement in advance should not be lightly undertaken. There will be advantage in appointing feudal princes.
""",
                1:"""nine: shows the difficulty its subject has in advancing. It will be advantageous for them to abide in the correct and firm; advantageous also to be made a feudal ruler.""",
                2:"""six: shows its subject distressed and obliged to return; even the horses of her chariot also seem to be retreating. But not by a despoiler is she assailed, rather by one who seeks her to be her wife. The young lady maintains her firm correctness, and declines a union. After ten years she will be united, and have children.""",
                3:"""six: shows one following the deer without the guidance of the forester, and only finding themselves in the midst of the forest. The superior person, acquainted with the secret risk, thinks it better to give up the chase. If they went forward, they would regret it. """,
                4:"""six: shows a lady, the horses of whose chariot appear to be in retreat. She seeks, however, the help of those who seek her to be their wife. Advance will be fortunate, all will turn out advantageously. """,
                5:"""nine: shows the difficulties in the way of the subject's dispensing the rich favours that might be expected from them. With firmness and correctness there will be good fortune in small things; but even with them, in great things there will be evil. """,
                6:"""six: shows its subject with the horses of their chariot obliged to retreat, and weeping tears of blood in streams."""
})

def in4data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id4data()",
                'title':""" 4. Mong / The Immature""", 
                'text':"""
The trigram representing a mountain, and beneath it that for a spring issuing forth, form Mong. The superior person, in accordance with this, strives to be resolute in their conduct and nourishes their virtue.

Mong indicates that there will be progress and success. I do not go and seek the youthful and inexperienced, but they come and seek me. When they show the sincerity that marks the first recourse to divination, I instruct them. If they apply a second and third time, that is troublesome; and I do not instruct the troublesome. There will be advantage in being firm and correct.
""",
                1:"""six: relates to to the dispelling of ignorance. It will be advantageous to use punishment for this purpose, and to remove the shackles from the mind. But going on in the way of punishment will give occasion for regret.""",
                2:"""nine: shows its subject exercising forbearance with the ignorant, in which there will be good fortune, and acknowleging of the goodness of those weaker, which will also be fortunate. They may be described also as a person able to sustain the burden of their family.""",
                3:"""six: seems to say that one should not partner a person whose emblem may be that when they see a person of wealth, they will not keep their person from them, and in no wise will advantage come from them. """,
                4:"""six: shows that if one is bound to an ignorant person, there will be occasion for regret. """,
                5:"""six: shows a simple person without experience. There will be good fortune. """,
                6:"""nine: we see one smiting the ignorant youth. But no advantage will come from doing them an injury. Advantage would come from warding off injury from them."""
})

def in5data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id5data()",
                'title':""" 5. Hsu / The Obstacles""", 
                'text':"""
The trigram for clouds ascending over that for the sky, form Hsu. The superior person, in accordance with this, eats and drinks, feasts and enjoys themselves as if there were nothing else to employ them.

Hsu intimates that, with the sincerity which is declared in it, there will be brilliant success. With firmness there will be good fortune ; and it will be advantageous to cross the great stream.
""",
                1:"""nine: shows its subject waiting in the distant border. It will be well for them constantly to maintain the purpose thus shown, in which case there will be no error.""",
                2:"""nine: shows its subject waiting on the sand of the mountain stream. They will suffer the small injury of being spoken against, but in the end there will be good fortune.""",
                3:"""nine: shows its subject in the mud close by the stream. They thereby invite the approach of injury. """,
                4:"""six: shows its subject waiting in the place of blood. But they will get out of the cavern. """,
                5:"""nine: shows its subject waiting amidst the appliances of a feast. Through their firmness and correctness there will be good fortune.""",
                6:"""six: shows its subject entered into the cavern. But there are three guests coming, to help them, without being urged. If they receive them respectfully, there will be good fortune in the end."""
})

def in6data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id6data()",
                'title':""" 6. Song / The Conflict""", 
                'text':"""
The trigram representing heaven and that representing water, moving away from each other, form Song. The superior person, in accordance with this, in the transaction of affairs takes good counsel about their first steps.

Song intimates how, though there is sincerity in one's contention, they will meet with opposition and obstruction; but if they cherish an apprehensive caution, there will be good fortune, while, if they must prosecute the contention to the bitter end, there will be evil. It will be advantageous to see the great person; it will not be advantageous to cross the great stream.
""",
                1:"""six: shows its subject not perpetuating the matter which the contention is about. He will suffer the small injury of being spoken against, but the end will be fortunate.""",
                2:"""nine: shows its subject keeping peace with three hundred families, and therefore falling into no mistake.""",
                3:"""six: shows its subject staying in the old place assigned for their support, and being firmly correct. Perilous as the position is, there will be good fortune in the end. Should they perchance engage in the king's business, they will not claim the merit of achievement. """,
                4:"""nine: shows its subject unequal to the contention. They return to the study of Heaven's ordinances, change their wish to contend and rest in being firm and correct. There will be good fortune. """,
                5:"""nine: shows its subject contending; and with great good fortune.""",
                6:"""nine: shows how its subject may have the leathern belt conferred on them by the sovereign, and thrice it shall be taken from them in a morning."""
})

def in7data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id7data()",
                'title':""" 7. Cheu / The Army""", 
                'text':"""
The trigram representing the earth and in the midst of it that representing water, form Cheu. The superior person, in accordance with this, nourishes and educates the people, and collects from among them the multitude of the armies.

Cheu indicates how, in the case which it purposes, with firmness and correctness, and a leader of age and experience, there will be good fortune and no error.
""",
                1:"""six: shows the army going forth according to the rules for such a movement. If these be not good, there will be evil. """,
                2:"""nine: shows the leader in the midst of the army. There will be good fortune and no error. The king has thrice conveyed to them the orders of their favour.""",
                3:"""six: shows how the army may, possibly, have inefficient leaders. There will be evil. """,
                4:"""six: shows the army in retreat. There is no error. """,
                5:"""six: shows birds in the fields, which it will be advantageous to seize and destroy. In that case there will be no error. If a learner leads the army, and inexperienced people idly occupy offices assigned to them, however firm and correct they may be, there will be evil. """,
                6:"""six: shows the great ruler delivering their charges, appointing some to be rulers of states, and others to undertake the leadership of clans ; but inferior people should not be employed in such positions."""
})

def in8data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id8data()",
                'title':""" 8. Pi / Concord""", 
                'text':"""
The trigram representing the earth, and over it that representing water, form Pi. The ancient kings, in accordance with this, established the various states and maintained an affectionate relation to their leaders.

Pi indicates that under the conditions which it supposes, there is good fortune. But let the principal party intended in it re-examine themselves, as if by divination, even if their virtue is great, unremitting, and firm. If it be so, there will be no error. Those who have no rest will then come to them; and with those who are too late in coming it will go ill.
""",
                1:"""six: shows its subject seeking by their sincerity to win the attachment of their target. There will be no error. Let the breast be full of sincerity as an earthenware vessel is of its contents, and it will in the end bring other advantages.""",
                2:"""six: we see the movement towards union and attachment proceeding from the inward mind. With firm correctness there will be good fortune.""",
                3:"""six: we see its subject seeking union with such as ought not be associated with. """,
                4:"""six: we see its subject seeking for union with the one beyond themself. With firm correctness there will be good fortune. """,
                5:"""nine: affords the most illustrious instance of seeking union and attachment. We seem to see in it the king urging his pursuit of the game only in three directions, and allowing the escape of all the animals before him, while the people of his towns do not warn one another to prevent it. There will be good fortune. """,
                6:"""six: we see one seeking union and attachment without having taken the first step to such an end. There will be evil."""
})

def in9data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id9data()",
                'title':""" 9. Siao Tch'ou / Accumulating Gradually""", 
                'text':"""
The trigram representing the sky, and that representing wind moving above it, form Siao Tch'ou. The superior person, in accordance with this, adorns the outward manifestation of their virtue.

Siao Tch'ou indicates that under its conditions there will be progress and success. We see dense clouds, but no rain coming from our borders in the west.
""",
                1:"""nine: shows its subject returning and pursuing their own course. What mistake could they fall into? There will be good fortune.""",
                2:"""nine: shows its subject, by the attraction of the former line, returning to the proper course. There will be good fortune.""",
                3:"""nine: suggests the idea of a carriage, the strap beneath which has been removed, or of a husband and wife looking on each other with averted eyes.""",
                4:"""six: shows its subject possessed of sincerity. The danger of bloodshed is thereby averted, and grounds for apprehension dismissed. There will be no mistake.""",
                5:"""nine: shows its subject possessed of sincerity, and drawing others to unite with them. Rich in resources, they employ their neighbours in the same cause with themselves. """,
                6:"""nine: shows how the rain has fallen, and the onward progress is stayed; so must we value the full accumulation of the virtue represented by the upper trigram. But a wife exercising excessive restraint, however firm and correct she may be, is in a position of peril, and like the moon approaching to the full. If the superior person prosecutes their measures in such circumstances, there will be evil."""
})

def in10data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id10data()",
                'title':""" 10. Li / Careful Conduct""", 
                'text':"""
The trigram representing the sky above, and below it that representing the waters of a marsh, form Li. The superior person, in accordance with this, discriminates between high and low, and gives settlement to the aims of all people.

Li suggests the idea of one treading on the tail of a tiger, which does not bite them. There will be progress and success.
""",
                1:"""nine: shows its subject treading their accustomed path. If they go forward, there will be no error.""",
                2:"""nine: shows its subject treading the path that is level and easy ; a quiet and solitary person, for whom, if they be firm and correct, there will be good fortune.""",
                3:"""six: shows a one-eyed person who thinks they can see well; a lame person who thinks they can walk well; one who treads on the tail of a tiger and is bitten. All this indicates ill fortune. We have a mere bravo acting the part of a great ruler. """,
                4:"""nine: shows its subject treading on the tail of a tiger. They become full of apprehensive caution, and in the end there will be good fortune.""",
                5:"""nine: shows the resolute tread of its subject. Though they be firm and correct, there will be peril. """,
                6:"""nine: tells us to look at the whole course that is trodden, and examine the presage which that gives. If it be complete and without failure, there will be great good fortune."""
})

def in11data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id11data()",
                'title':""" 11. T'ai / Peace, Restful Fluidity""", 
                'text':"""
The trigrams for heaven and earth in communication together form T'ai. The sage sovereign, in harmony with this, fashions and completes their regulations after the courses of heaven and earth, and assists the application of the adaptations furnished by them, in order to benefit the people.

In T'ai we see the small gone and the great coming. It indicates that there will be good fortune, with progress and success.
""",
                1:"""nine: suggests the idea of grass pulled up, and bringing with it other stalks with whose roots it is connected. Advance on the part of its subject will be fortunate.""",
                2:"""nine: shows one who can empathise with the uncultivated, will cross the Ho without a boat, does not forget the distant, and has no selfish friendships. Thus do they prove themselves to be acting in accordance with the course of correctness.""",
                3:"""nine: shows that, while there is no state of peace that is not liable to be disturbed, and no departure of evil people so that they shall not return, yet when one is firm and correct, as one realises the distresses that may arise, one will commit no error. There is no occasion for sadness at the certainty of such recurring changes; and in this mood the happiness of the present may be long enjoyed. """,
                4:"""six: shows its subject fluttering down; not relying on their own rich resources, bur calling in their neighbours. They all come not as having received warning, but in the sincerity of their hearts. """,
                5:"""six: reminds us of king Ti-yi's rule about the marriage of his younger sister. By such a course there is happiness and there will be great good fortune. """,
                6:"""six: shows us the city wall returned into the moat. It is not the time to use the army. The subject of the line may, indeed, announce their orders to the people of their own city; but however correct and firm they may be, they will have cause for regret."""
})

def in12data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id12data()",
                'title':""" 12. P'i / Stagnation, Obstruction""", 
                'text':"""
The trigrams of heaven and earth, not in intercommunication, form P'i. The superior person, in accordance with this, restrains the manifestation of their virtue, and avoids the calamities that threaten them. There is no opportunity of conferring on them the glory of reward in their employment.

In P'i there is the want of good understanding between people at different levels of development, and its indication is unfavourable to the firm and correct course of the superior person. We see in it the great gone and the small comming.
""",
                1:"""six: suggests the idea of grass pulled up, and bringing with it other stalks with whose roots it is connected. With firm correctness on the part of its subject, there will be good fortune and progress.""",
                2:"""six: shows its subject as patient and obedient. The small person is comporting themselves so there will be good fortune. If the great person comports themself as the distress and obstruction require, they will have success.""",
                3:"""six: shows its subject ashamed of the purpose folded in their breast.""",
                4:"""nine: shows its subject acting in accordance with the ordination of Heaven, and committing no error. Their companions will come and share in their happiness.""",
                5:"""nine: we see they who bring the distress and obstruction to a close, the person great and fortunate. But let them say, 'We may perish! We may perish !', so shall the state of things become firm, as if bound to a clump of bushy mulberry trees.""",
                6:"""nine: shows the overthrow and removal of the condition of distress and obstruction. Before this there was that condition. Hereafter there will be joy."""
})

def in13data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id13data()",
                'title':""" 13. Tong Jen / Community""", 
                'text':"""
The trigrams for heaven and fire form Tong Jen. The superior person, in accordance with this, distinguishes things according to their kinds and levels.

Tong Jen or 'Community' appears here as we find it in the remote district of the country, indicating progress and success. It will be advantageous to cross the great stream. It will be advantageous to maintain the firm correctness of the superior person.
""",
                1:"""nine: shows the representative of the community just issuing from their gate. There will be no error.""",
                2:"""six: shows the representative of the community in relation with their kindred. There will be occasion for regret.""",
                3:"""nine: shows its subject with their arms hidden in the thick grass, and at the top of a high mound. But for three years they make no demonstration.""",
                4:"""nine: shows its subject mounted on the city wall; but they do not proceed to make the attack they contemplate. There will be good fortune.""",
                5:"""nine: the representative of the community first wails and cries out, and then laughs. Their great host conquers, and they and the subject of the second line meet together. """,
                6:"""nine: shows the representative of the community in the suburbs. There will be no occasion for repentance."""
})

def in14data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id14data()",
                'title':""" 14. Ta You / Big Strength""", 
                'text':"""
The trigram for heaven and that of fire above it form Ta You. The superior person, in accordance with this, represses what is evil and gives distinction to what is good, in sympathy with the excellent Heaven-conferred nature.

Ta You indicates that, under the circumstances which it implies, there will be great progress and success.
""",
                1:"""nine: there is no approach to what is injurious, and there is no error. Let there be a realisation of the difficulty and danger of the position, and there will be no error to the end.""",
                2:"""nine: we have a large wagon with its load. In whatever direction advance is made, there will be no error.""",
                3:"""nine: shows us a feudal prince presenting their offerings to the Son of Heaven. A small person would be unequal to such a duty. """,
                4:"""nine: shows its subject keeping their great resources under restraint. There will be no error. """,
                5:"""six: shows the sincerity of its subject reciprocated by that of all the others represented in the hexagram. Let them display a proper majesty, and there will be good fortune.""",
                6:"""nine: shows its subject with help accorded to them from Heaven. There will be good fortune, advantage in every respect."""
})

def in15data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id15data()",
                'title':""" 15. Tchien / Modesty""", 
                'text':"""
The trigram for the earth and that of a mountain in the midst of it form Tchien. The superior person, in accordance with this, diminishes what is excessive in their being, and improves where there is any defect, bringing about an equality, according to the nature of the case, in their treatment of themselves and others.

Tchien indicates progress and success. The superior person, being humble as it implies, will have a good issue from their understandings.
""",
                1:"""six: shows us the superior person who adds humility to humility. Even the great stream may be crossed with this, and there will be good fortune.""",
                2:"""six: shows us humility that has made itself recognised. With firm correctness there will be good fortune.""",
                3:"""nine: bows to the superior person of acknowledged merit. They will maintain their success to the end, and have good fortune. """,
                4:"""six: shows one, whose action would be in every way advantageous, bringing forth even more their humility. """,
                5:"""six: shows one who, without bring rich, is able to employ their neighbours. He may advantageously use the force of arms. All their movements will be advantageous. """,
                6:"""six: shows us humility that has made itself recognised. The subject of it will with advantage put their hosts in motion; but they will only punish their own towns and state."""
})

def in16data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id16data()",
                'title':""" 16. Yu / Majesty in Connection""", 
                'text':"""
The trigrams for the earth, and thunder issuing from it with its crashing noise, form Yu. The ancient kings, in accordance with this, composed their music and did honour to virtue, presenting it especially and most grandly to the supreme being, when they associated with it at the service of their highest ancestor and their parents.

Yu indicates that, in the state which it implies, feudal princes may be set up, and the hosts put in motion, with advantage.
""",
                1:"""six: shows its subject proclaiming their pleasure and satisfaction. There will be evil.""",
                2:"""six: shows one who is firm as a rock. They see a thing without waiting till it has come to pass; with their firm correctness there will be good fortune.""",
                3:"""six: shows one looking up for favours, while they indulge the feeling of pleasure and satisfaction. They must understand! If they be late in repenting, there will indeed be occasion for repentance. """,
                4:"""nine: shows they from whom harmony and satisfaction come. Great is the success which they obtain. Let them not allow suspicions to enter their mind, and thus friends will gather around them.""",
                5:"""six: shows one with a chronic complaint, but who lives on without dying.""",
                6:"""six: shows its subject with darkened mind devoted to the pleasure and satisfaction of the time; but if they change their course even when it may be considered as completed, there will be no error."""
})

def in17data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id17data()",
                'title':""" 17. Souei / Submission to the Duty""", 
                'text':"""
The trigram for the waters of a marsh and that for thunder hidden in the midst of it, form Souei. The superior person in accordance with this, when it is getting toward dark, enters their house and rests.

Souei indicates that under its conditions there will be great progress and success. But it will be advantageous to be firm and correct. There will then be no error.
""",
                1:"""nine: shows us one changing the object of their pursuit, but if they are firm and correct, there will be good fortune. Going beyond their own gate to find associates, they will achieve merit.""",
                2:"""six: shows us one who cleaves to the little child, and lets go the person of age and experience.""",
                3:"""six: shows us one who cleaves to the person of age and experience, and lets go the little child. Such following will get what it seeks; but it will be advantageous to adhere to what is firm and correct.""",
                4:"""nine: shows us one followed, and obtaining adherents. Though they be firm and correct, there will be evil. If they be sincere however in their course, and make that evident, into what error can they fall? """,
                5:"""nine: shows us the ruler sincere in fostering all that is excellent. There will be good fortune. """,
                6:"""six: shows us sincerity firmly held and clung to, yea, and bound fast. We see the king with this presenting his offerings on the western mountain."""
})

def in18data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id18data()",
                'title':""" 18. Kou / Toward Corruption""",   
                'text':"""
The trigram for a mountain, and below it that for wind, form Kou. The superior person, in accordance with this, nourishes their own virtue and helps the people.

Kou indicates great progress and success to them who deals properly with the condition represented by it. There will be advantage in efforts like that of crossing the great stream. One should weigh well, however, the events of three days before the turning point, and those to be done three days after it.
""",
                1:"""six: shows a child dealing with the troubles caused by their father. If they be an able child, the father will escape the blame of having erred. The position is perilous, but there will be good fortune in the end.""",
                2:"""nine: shows a child dealing with the troubles caused by their mother. They should not carry their firm correctness to the utmost.""",
                3:"""nine: shows a child dealing with the troubles caused by their father. There may be some small occasion for repentance, but there will not be any great error.""",
                4:"""six: shows a child viewing indulgently the troubles caused by their father. If they go forward, they will find cause to regret it.""",
                5:"""six: shows a child dealing with the troubles caused by their father. They obtain the praise of using the fit instrument for their work. """,
                6:"""nine: shows us one who does not serve either king or feudal lord, whose lofty spirit prefers to attend to their own affairs."""
})

def in19data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id19data()",
                'title':""" 19. Lin / Approach""", 
                'text':"""
The trigram for the waters of a marsh and that for the earth above it form Lin. The superior person, in accordance with this, has their purpose of instruction that is inexhaustible, and which nourishes and supports the people without limit.

Lin indicates that under the conditions supposed in it there will be great progress and success, while it will be advantageous to be firmly correct. In the eighth month there will be evil.
""",
                1:"""nine: shows its subject advancing in company with the subject of the second line. Through their firm correctness there will be good fortune.""",
                2:"""nine: shows its subject advancing in company with the subject of the first line. There will be good fortune; advancing will be in every way advantageous.""",
                3:"""six: shows one well pleased indeed to advance, but whose action will be in no way advantageous. If they become anxious about it however, there will be no error. """,
                4:"""six: shows one advancing in the highest mode. There will be no error.""",
                5:"""six: shows the advance of wisdom, such as befits the great ruler. There will be good fortune.""",
                6:"""six: shows the advance of honesty and generosity. There will be good fortune, and no error.""",
})

def in20data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id20data()",
                'title':""" 20. Kouan / Looking Down""", 
                'text':"""
The trigrams representing the earth, and that for wind moving above it, form Kouan. The ancient kings, in accordance with this, examined the different regions of the kingdom, to see the ways of the people, and set forth their instructions.

Kouan shows how they whom it represents should be like the worshipper who has washed their hands, but not yet presented their offering; with sincerity and appearance of dignity, commanding reverent regard.
""",
                1:"""six: shows the appearances of a child; not blameable in one of inferior level, but a matter for regret in a superior person.""",
                2:"""six: shows one peeping out from a door. It would be advantageous if it were merely the firm correctness of a female.""",
                3:"""six: shows one looking at the course of their own life, to advance or recede accordingly. """,
                4:"""six: shows one contemplating the glory of the kingdom. It will be advantageous for them, being such as they are, to seek to be a guest of the king.""",
                5:"""nine: shows its subject contemplating their own life-course. Being a superior person, they will thus fall into no error. """,
                6:"""nine: shows its subject contemplating their character to see if it is indeed that of a superior person. They will not fall into error."""
})

def in21data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id21data()",
                'title':""" 21. Che Ho / Bite Through""", 
                'text':"""
The trigrams representing thunder and lightning form Che Ho. The ancient kings, in accordance with this, framed their penalties with intelligence, and promulgated their laws.

Che Ho indicates successful progress in the condition of things which it supposes. It will be advantageous to use legal constraints.
""",
                1:"""nine: shows one with their feet in the stocks and deprived of their toes. There will be no error.""",
                2:"""six: shows one biting through the soft flesh, and going on to bite off the nose. There will be no error.""",
                3:"""six: shows one gnawing dried flesh, and meeting with what is disagreeable. There will be occasion for some small regret, but no great error.""",
                4:"""nine: shows one gnawing the flesh dried on the bone, and getting the pledges of money and arrows. It will be advantageous to them to realise the difficulty of their task and be firm, in which case there will be good fortune. """,
                5:"""six: shows one gnawing at the firm and correct, realising the peril of their position. There will be no error.""",
                6:"""nine: shows one wearing the yoke, and deprived of their ears. There will be evil."""
})

def in22data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id22data()",
                'title':""" 22. Pi / Elegance""", 
                'text':"""
The trigram representing a mountain with that for fire under it form Pi. The superior person, in accordance with this, throws a brilliancy around their various processes of government, but does not dare in a similar way to decide cases of criminal litigation.

Pi indicates that there should be free course in what it denotes. There will be little advantage however if it be allowed to advance and take the lead.
""",
                1:"""nine: shows one adorning the way of their feet. They can discard a carriage and walk on foot.""",
                2:"""six: shows one adorning their beard.""",
                3:"""nine: shows its subject with the appearance of being adorned and bedewed with rich favours. But let them ever maintain their firm correctness, and there will be good fortune.""",
                4:"""six: shows one looking as if adorned, but only in white. As if mounted on a white horse, and furnished with wings, they seek union with the subject of the first line, while the intervening third pursues, not as a robber, but intent on a matrimonial alliance. """,
                5:"""six: shows its subject adorned by the occupants of the heights and gardens. They bear their roll of silk, small and slight. They may appear stingy; but there will be good fortune in the end.""",
                6:"""nine: has its subject with white as their only ornament. There will be no error."""
})

def in23data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id23data()",
                'title':""" 23. Po / Bursting""", 
                'text':"""
The trigram representing the earth, and above it that for a mountain which adheres to the earth, form Po. Superiors, in accordance with this, seek to strengthen those below them, to secure the peace and stability of their own position.

Po indicates that in the state which it symbolises it will not be advantageous to make a movement in any direction whatever.
""",
                1:"""six: shows one overturning the couch by injuring its legs. The injury will go on to the destruction of all firm correctness, and there will be evil.""",
                2:"""six: shows one overthrowing the couch by injuring its frame. The injury will go on to the destruction of all firm correctness, and there will be evil.""",
                3:"""six: shows its subject among the overthrowers; but there will be no error. """,
                4:"""six: shows its subject having overthrown the couch, and going to injure the skin of they who lie on it. There will be evil. """,
                5:"""six: shows its subject leading on the others like a string of fishes, and obtaining for them the favour that lights on the inmates of the palace. There will be advantage in every way. """,
                6:"""nine: shows as a great fruit which has not been eaten. The superior person finds the people again as a chariot carrying them. The small people by their course overthrow their own dwellings."""
})

def in24data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id24data()",
                'title':""" 24. Fou / The Return, Amendment""", 
                'text':"""
The trigram representing the earth, and that for thunder in the midst of it, form Fou. The ancient kings, in accordance with this, on the day of the winter solstice, shut the gates of the passes from one state to another, so that the travelling merchants could not then pursue their journeys, nor the princes go on with the inspection of their states.

Fou indicates that where will be free course and progress in what it denotes; the subject of it finds no one to distress them in their exits and entrances; friends come to them, and no error is committed. They will return and repeat their proper course. In seven days comes their return. There will be advantage in whatever direction movement is made.
""",
                1:"""nine: shows its subject returning from an error of no great extent, which would not proceed to anything requiring repentance. There will be great good fortune.""",
                2:"""six: shows the admirable return of its subject. There will be good fortune.""",
                3:"""six: shows one who has made repeated returns. The position is perilous, but there will be no error. """,
                4:"""six: shows its subject moving right in the centre among those represented by the other divided lines, and yet returning alone to their proper path.""",
                5:"""six: shows the noble return of its subject. There will be no ground for repentance. """,
                6:"""six: shows its subject all astray on the subject of returning. There will be evil. There will be calamities and errors. If with their views they put the hosts in motion, the end will be a great defeat, whose issues will extend to the ruler of the state. Even in ten years they will not they able to repair the disaster."""
})

def in25data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id25data()",
                'title':""" 25. Wou Wang / Integrity""", 
                'text':"""
The thunder rolls all under the sky, and to everything there is given its nature, free from all insincerity. The ancient kings, in accordance with this, made their regulations in complete accordance with the seasons, thereby nourishing all things.

Wou Wang indicates great progress and success, while there will be advantage in being firm and correct. If its subject and their action be not correct, they will fall into errors, and it will not be advantageous for them to move in any direction.
""",
                1:"""nine: shows its subject free from all insincerity. Their advance will be accompanied with good fortune.""",
                2:"""six: shows one who reaps and gathers the produce of their third year's fields without having cultivated them the first year for that end. To such a one there will be advantage in whatever direction they may move.""",
                3:"""six: shows calamity happening to one who is free from insincerity; as in the case of an ox that has been tied up: a passer by finds it and carries it off, while the people in the neighbourhood have the calamity of being accused and apprehended.""",
                4:"""nine: shows a case in which, if its subject can remain firm and correct, there will be no error. """,
                5:"""nine: shows one who is free from insincerity, and yet has fallen ill. Let them not use medicine, and they will have occasion for joy in their recovery.""",
                6:"""nine: shows its subject free from insincerity, yet sure to fall into error if they take action. Their action will not be advantageous in any way."""
})

def in26data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id26data()",
                'title':""" 26. Ta Tch'ou / The Great Accumulating""", 
                'text':"""
The trigram representing a mountain, and in the midst of it that representing heaven, form Ta Tch'ou. The superior person, in accordance with this, remembers the words and deeds of former people, to assist in the accumulation of their virtue.

Under the condition of Ta Tch'ou it will be advantageous to be firm and correct. If its subject does not seek to enjoy their revenues in their own family without taking service at court, there will be good fortune. It will be advantageous for them to cross the great stream.
""",
                1:"""nine: shows its subject in a position of peril. It will be advantageous for them to stop their advance.""",
                2:"""nine: shows a carriage with the strap under it removed.""",
                3:"""nine: shows its subject urging their way with good horses. It will be advantageous for them to realise the difficulty of their course, and to be firm and correct, exercising themselves daily in their charioteering and methods of defence; then there will be advantage in whatever direction they may advance. """,
                4:"""six: shows the young bull, yet it has a piece of wood over its horns. """,
                5:"""six: shows the teeth of a castrated hog. There will be good fortune. """,
                6:"""nine: shows itself in command of the firmament of heaven. There will be progress."""
})

def in27data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id27data()",
                'title':""" 27. I / Nourishment""", 
                'text':"""
The trigram representing a mountain, and under it that for thunder, form I. The superior person, in accordance with this, enjoins watchfulness over our words, and the temperate regulation of our eating and drinking.

I indicates that with firm correctness there will be good fortune in what is denoted by it. We must look at what we are seeking to nourish, and by the exercise of our thoughts seek for the proper nourishment.
""",
                1:"""nine: seems to be thus addressed,  'You doubt your own effective gifts, and look at me with your mouth turned down with envy.' There will be evil.""",
                2:"""six: shows one looking downward for nourishment, which is contrary to what is proper: or seeking it from the height above, advance towards which will lead to evil. """,
                3:"""six: shows one acting contrary to the method of nourishing. However firm they may be, there will be evil. For ten years let them not take any action, for it will not be in any way advantageous. """,
                4:"""six: looks downwards like a tiger for the power to nourish. There will be good fortune. Looking with a tiger's downward unwavering glare, and with their desire that impels them to spring after spring, they will fall into no error.""",
                5:"""six: shows one acting contrary to what is regular and proper; but if they abide in firmness, there will be good fortune. They should not, however, try to cross the great stream.""",
                6:"""nine: shows they from whom comes the nourishing. One's position is perilous, but there will be good fortune. It will be advantageous to cross the great stream."""
})

def in28data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id28data()",
                'title':""" 28. Ta Kouo / Excess""", 
                'text':"""
The trigram representing trees, hidden beneath that for the waters of a marsh, form Ta Kouo. The superior person, in accordance with this, stands up alone and has no fear, and stays retired from the world without regret.

Ta Kouo suggest to us a beam that is weak. There will be advantage in moving under these conditions in any directions whatever; there will be success.
""",
                1:"""six: shows one placing mats of the dried grass under things set on the ground. There will be no error.""",
                2:"""nine: shows a decayed willow producing shoots. There will be advantage in every way.""",
                3:"""nine: shows a beam that is weak. There will be evil.""",
                4:"""nine: shows a beam curving upwards. There will be good fortune. If the subject of it looks for support elsewhere, there will be cause for regret. """,
                5:"""nine: shows a decayed willow producing flowers. There will be occasion neither for blame nor for praise. """,
                6:"""six: shows its subject with extraordinary boldness wading through a stream, till the water hides the crown of their head. There will be evil, but no ground for blame."""
})

def in29data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id29data()",
                'title':""" 29. K'an / The Abyss, Danger""", 
                'text':"""
The representation of water flowing on continuously forms the repeated K'an. The superior person, in accordance with this, maintains constantly the virtue of their heart and the integrity of their conduct, and practises the business of instruction.

K'an, here repeated, shows the possession of sincerity, though which the mind is penetrating. Action in accordance with this will be of high value.
""",
                1:"""six: shows its subject in the double abyss, and yet entering a cavern within it. There will be evil.""",
                2:"""nine: shows its subject in all the peril of the abyss. They will, however, get a little of the deliverance that they seek.""",
                3:"""six: shows its subject, whether they come or go, descend or ascend, confronted by an abyss. All is peril to them and unrest. Their endeavours will lead them into the cavern of the pit. There should be no action in such a case.""",
                4:"""six: shows its subject at a feast, with simply a bottle of spirits and a subsidiary basket of rice, while the cups and howls are only of earthenware. The important lessons are introduced as their ruler's intelligence admits. There will in the end be no error.""",
                5:"""nine: shows the water of the abyss not yet full, so that it might flow away; but order will soon be brought about. There will be no error. """,
                6:"""six: shows its subject bound with cords of three strands or two strands, and placed in a thicket of thorns. Still in three years they do not learn the course for them to pursue. There will be evil."""
})

def in30data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id30data()",
                'title':""" 30. Li / Strength and Beauty""", 
                'text':"""
The trigram for brightness, repeated, forms Li. The great person, in accordance with this, cultivates more and more their brilliant virtue, and diffuses its brightness over the four quarters of the land.

Li indicates that, in regard to what it denotes, it will be advantageous to be firm and correct, and that thus there will be a free course and success.
""",
                1:"""nine: shows one ready to move with confused steps. But they tread at the same time reverently, and there will be no mistake.""",
                2:"""six: shows its subject in their place in yellow. There will be great good fortune.""",
                3:"""nine: shows its subject in a position like that of the declining sun. Instead of playing on their instrument of earthenware, and singing, they utter the groans of an old person of eighty. There will be evil. """,
                4:"""nine: shows the manner of its subject's arrival. How abrupt it is, as with fire, as with death, thus to be rejected by all. """,
                5:"""six: shows one with tears flowing in torrents, and groaning in sorrow. There will be good fortune. """,
                6:"""nine: shows the king employing the subject in his punitive expeditions. Achieving admirable merit, they break only the chief of the rebels. Where their prisoners were not their associates, they do not punish. There will be no error.""",
})

def in31data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id31data()",
                'title':""" 31. Hsien / Attraction""", 
                'text':"""
The trigram representing a mountain, and above it that for the waters of a marsh, form Hsien. The superior person, in accordance with this, keeps their mind free from pre-occupations, and open to receive the influence of others.

Hsien indicates that, on the fulfilment of the conditions implied in it, there will be a free course and success. Its advantage will depend on being firm and correct, as in marrying suitably. There will be good fortune.
""",
                1:"""six: shows one moving their big toes.""",
                2:"""six: shows one moving the calves of their leg. There will be evil. If they abide quietly in their place, there will be good fortune.""",
                3:"""nine: shows one moving their thighs, and keeping close hold of those whom they follow. Going forward in this way will cause regret. """,
                4:"""nine: shows that they will be unsettled in their movements, only their friends will follow their purpose.""",
                5:"""nine: shows one moving the flesh along the spine above the heart. There will be no occasion for repentance. """,
                6:"""six: shows one moving their jaws and tongue."""
})

def in32data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id32data()",
                'title':""" 32. Hong / The Long Enduring""", 
                'text':"""
The trigram representing thunder and that for wind form Hong. The superior person, in accordance with this, stands firm, and does not change their method of operation.

Hong indicates successful progress and no error in what it denotes. But the advantage will come from being firm and correct; and movement in any direction whatever will be advantageous.
""",
                1:"""six: shows its subject deeply desirous of long continuance. Even with firm correctness there will be evil; there will be no advantage in any way.""",
                2:"""nine: shows all occasion for repentance disappearing.""",
                3:"""nine: shows one who does not continuously maintain their virtue. There are those who will impute this to them as a disgrace. However firm they may be, there will be grounds for regret """,
                4:"""nine: shows a field where there is no game. """,
                5:"""six: shows its subject continuously maintaining the virtue indicated by it. In a wife this will be fortunate; in a husband, evil.""",
                6:"""six: shows its subject exciting themself to long continuance. There will be evil."""
})

def in33data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id33data()",
                'title':""" 33. Toun / Withdrawal""", 
                'text':"""
The trigram representing the sky, and below it that for a mountain, form Toun. The superior person, in accordance with this, keeps small people at distance, not showing that they dislike them, except by their own dignified gravity.

Toun indicates successful progress in its circumstances. To a small extent it will still be advantageous to be firm and correct.
""",
                1:"""six: shows a withdrawing tail. The position is perilous. No movement in any direction should they made. """,
                2:"""six: shows its subject holding their purpose fast as if by a thong made from the hide of a yellow ox, which cannot they broken.""",
                3:"""nine: shows one withdrawing but bound, to their distress and peril. If they were to deal with their hinderances as in nourishing a servant or concubine, it would be fortunate for them. """,
                4:"""nine: shows its subject withdrawing, notwithstanding their likings. In a superior person this will lead to good fortune; a small person cannot attain to this. """,
                5:"""nine: shows its subject withdrawing in an admirable way. With firm correctness there will be good fortune. """,
                6:"""nine: shows its subject withdrawing in a noble way. It will be advantageous in every respect."""
})

def in34data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id34data()",
                'title':""" 34. Ta Tch'ouang / Big Strength""", 
                'text':"""
The trigram representing heaven, and above it that for thunder, form Ta Tch'ouang. The superior person, in accordance with this, does not take a step which is not according to propriety.

Ta Tch'ouang indicates that under the conditions which it symbolises it will be advantageous to be firm and correct.
""",
                1:"""nine: shows its subject manifesting their strength in their toes, but advance will lead to evil, most certainly.""",
                2:"""nine: shows that with firm correctness there will be good fortune.""",
                3:"""nine: shows the case of one small person using all their strength; and the case of a superior person, whose rule is not to use all their strength. Even with firm correctness the position would be perilous. The exercise of strength in it might then compared to the case of a ram butting against a fence, and getting their horns entangled. """,
                4:"""nine: shows a case in which firm correctness leads to good fortune, and occasion for repentance disappears. We see the fence openned without the horns being entangled. The strength is like that in the wheel-spokes of a large waggon.""",
                5:"""six: shows one who loses their ram-like strength in the ease of their position, but there will be no occasion for repentance.""",
                6:"""six: shows one who may be compared to the ram butting against the fence, and unable either to retreat, or to advance as they would fain do. There will not be advantage in any respect; but if they realise the difficulty of their position, there will be good fortune."""
})

def in35data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id35data()",
                'title':""" 35. Tchin / Progress""", 
                'text':"""
The trigram representing the earth, and that for the bright sun coming forth above it, form Tchin. The superior person, according to this, gives themself to making more brilliant their bright virtue.

In Tchin we see a prince who secures the tranquillity of the people presented in reward with numerous horses by the king, and three times in a day received at interviews.
""",
                1:"""six: shows one wishing to advance, and at the same time kept back. Let them be firm and correct, and there will be good fortune. If trust does not abide in them, let them maintain a large and generous mind, and there will be no error.""",
                2:"""six: shows its subject with the appearance of advancing, and yet of being sorrowful. If they be firm and correct, there will be good fortune. They will receive this great blessing from their grandmother.""",
                3:"""six: shows its subject trusted by all around them. All occasion for repentance will disappear. """,
                4:"""nine: shows its subject, however firm and correct they may be, in a position of peril.""",
                5:"""six: shows how all occasion for repentance disappears from its subject, but let them not concern themselves about whether they shall fail or succeed. To advance will be fortunate, and in every way advantageous.""",
                6:"""nine: shows one advancing their horns. But they only use them to punish the rebellious people of their own city. The position is perilous, but there will be good fortune. Still, however firm and correct they may be, there will be occasion for regret."""
})

def in36data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id36data()",
                'title':""" 36. Ming Yi / The Darkening of the Light""", 
                'text':"""
The trigram representing the earth, and that for the bright sun entering within it, form Ming Yi. The superior person, in accordance with this, conducts their management of people thusly; they show their intelligence by keeping it obscured.

Ming Yi indicates that in the circumstances which it denotes, it will be advantageous to realise the difficulty of the position, and maintain firm correctness.
""",
                1:"""nine: shows its subject, in the condition indicated by Ming Yi, flying, but with drooping wings. When the superior person is considering their going away, they may be for three days without eating. Wherever they go, the people there may speak derisively of them.""",
                2:"""six: shows its subject, in the condition indicated by Ming Yi, wounded in the left thigh. They save themselves by the strength of a swift horse; and are fortunate.""",
                3:"""nine: shows its subject, in the condition indicated by Ming Yi, hunting in the south, and taking the great chief of the darkness. They should not be eager to make all correct at once.""",
                4:"""six: shows its subject just entered into the left side of the belly of the dark land. But they are able to carry out the attitude appropriate in the condition indicated by Ming Yi, quitting the gate and courtyard of the lord of darkness.""",
                5:"""six: shows how a great person fulfilled the condition indicated by Ming Yi. It will be advantageous to be firm and correct. """,
                6:"""six: shows the case where there is no light, but only obscurity. Its subject had at first ascended to the top of the sky; their future shall be to go into the earth."""
})

def in37data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id37data()",
                'title':""" 37. Tchia Jen / The Family""", 
                'text':"""
The trigram representing fire, and that for wind coming forth from it, form Tchia Jen. The superior person, in accordance with this, orders their word according to the truth of things, and their conduct so that it is uniformly consistent.

For the realisation of what is taught in Tchia Jen, or for the regulation of the family, what is most advantageous is that the wife be firm and correct.
""",
                1:"""nine: shows its subject establishing restrictive regulations in their household. Occasion for repentance will disappear.""",
                2:"""six: shows its subject taking nothing on herself, but in her central place attending to the preparation of the food. Through her firm correctness there will be good fortune.""",
                3:"""nine: shows its subject treating the members of the household with sternness, there will be peril, but there will also be good fortune. If the wife and children were to besmirking and chattering, in the end there would be occasion for regret. """,
                4:"""six: shows its subject enriching the family. There will be great good fortune.""",
                5:"""nine: shows the influence of the king extending to their family. There need be no anxiety; there will be good fortune. """,
                6:"""nine: shows its subject possessed of sincerity and arrayed in majesty. In the end there will be good fortune."""
})

def in38data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id38data()",
                'title':""" 38. K'ouei / Opposition""", 
                'text':"""
The trigram representing fire above, and that for the waters of a marsh below, form K'ouei. The superior person, in accordance with this, where there is a general agreement, yet admits diversity.

K'ouei indicates that, notwithstanding the condition of things which it denotes, in small matters there will still be good success.
""",
                1:"""nine: shows that for its subject occasion for repentance will disappear. They have lost their horses, but let them not seek for them; they will return of themselves. Should they meet with bad people, they will not err in communicating with them.""",
                2:"""nine: shows its subject happening to meet with their lord in a bye-passage. There will be no error.""",
                3:"""six: shows one whose carriage is dragged back, while the oxen in it are pushed back, and they are themselves subjected to the shaving of their head and the cutting off of their nose. There is no good beginning, but there will be a good end.""",
                4:"""nine: shows its subject solitary amidst the prevailing disunion, but they meet with the good person represented by the first line, and they blend their sincere desires together. The position is one of peril, but there will be no mistake.""",
                5:"""six: shows that for its subject occasion for repentance will disappear. With their relative and minister they unite closely and readily as if they were biting through a piece of skin. When they go forward with this help, what error could there be? """,
                6:"""nine: shows its subject solitary amidst the prevailing disunion. In the subject of the third line, they seem to see a pig bearing on its back a load of mud, or fancy there is a carrriage full of ghosts. They first bend their bow against them, and afterwards unbend it, for they discover that there is not an assailant to injure, but a near relative. Going forward, they shall meet with genial rain, and there will be good fortune."""
})

def in39data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id39data()",
                'title':""" 39. Tch'ien / Trouble""", 
                'text':"""
The trigram representing a mountain, and above it that for water, form Tch'ien. The superior person, in accordance with this, turns round and examines themself, and cultivates their virtue.

In the state indicated by Tch'ien advantage will be found in the south-west, and the contrary in the north-east. It will be advantageous also to meet with the great person. In these circumstances, with firmness and correctness, if some operation be called for, there will be good fortune.
""",
                1:"""six: shows that advance on the part of its subject will lead to greater difficulties, while remaining stationary will afford ground for praise.""",
                2:"""six: shows the minister of the king struggling with difficulty on difficulty, and not with a view to their own advantage.""",
                3:"""nine: shows its subject advancing, but only to greater difficulties. They remain stationary, and return to their former associates.""",
                4:"""six: shows its subject advancing, but only to greater difficulties. They remain stationary, and unite with the subject of the line above.""",
                5:"""nine: shows its subject struggling with the greatest difficulties, while friends are coming to help them. """,
                6:"""six: shows its subject going forward, only to increase the difficulties, while their remaining stationary will be productive of great merit. There will be good fortune, and it will be advantageous to meet with the great person."""
})

def in40data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id40data()",
                'title':""" 40. Tchieh / The Release, The Outcome""", 
                'text':"""
The trigram representing thunder and that for rain, with these phenomena in a state of manifestation, form Tchieh. The superior person, in accordance with this, forgives errors, and deals gently with crimes.

In the state indicated by Tchieh advantage will be found in the south-west. If no further operations are called for, there will be good fortune in coming back to the earlier conditions and good fortune in the early progression of them.
""",
                1:"""six: shows that its subject will commit no error.""",
                2:"""nine: shows its subject catching, in hunting, three foxes, and obtaining the golden arrows. With firm correctness there will be good fortune.""",
                3:"""six: shows a porter with their burden, yet riding in a carriage. They will only tempt robbers to attack them. However firm and correct they may try to be, there will be cause for regret.""",
                4:"""nine: says of its subject, 'Remove your toes. Friends will then come, between you and they there will be mutual confidence.'""",
                5:"""six: shows its subject, the superior person, executing their function of removing whatever is injurious to the idea of the hexagram, in which case there will be good fortune, and confidence in them will be shown even by the small people. """,
                6:"""six: shows a feudal prince with their bow shooting at a falcon on the top of a high wall, and hitting it. The effect of their action will be in every way advantageous."""
})

def in41data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id41data()",
                'title':""" 41. Soun / Reduction""", 
                'text':"""
The trigram representing a mountain, and beneath it that for the waters of a marsh, form Soun. The superior person, in accordance with this, restrains their wrath and controls their desires.

In what is denoted by Soun, if there be sincerity in they who employs it, there will be great good fortune: freedom for error; firmness and correctness that can be maintained; an advantage in every movement that shall be made. In what shall this sincerity in the exercise of Soun be employed? Even in sacrifice, two baskets of grain, though there be nothing else, may be presented.
""",
                1:"""nine: shows its subject suspending their own affairs, and hurrying away to help the subject of the fourth line. They will commit no error, but let them consider how far they should contribute of what is theirs for the other.""",
                2:"""nine: shows that it will be advantageous for its subject to maintain a firm correctness, and that action on their part will be evil. They can give increase to their correlate without taking from themselves.""",
                3:"""six: shows how, of three people walking together, the number is diminished by one; and how one, walking, finds their friend. """,
                4:"""six: shows its subject diminishing the ailment under which they labour by making the subject of the first line hasten to their help, and making them glad. There will be no error. """,
                5:"""six: shows parties adding to the stores of its subject ten pairs of tortoise shells, and accepting no refusal. There will be great good fortune.""",
                6:"""nine: shows its subject giving increase to others without taking from themselves. There will be no error. With firm correctness there will be good fortune. There will be advantage in every movement that shall be made. They will find ministers more than can be counted by their clans."""
})

def in42data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id42data()",
                'title':""" 42. Yi / Increase""", 
                'text':"""
The trigram representing wind and that for thunder form Yi. The superior person, in accordance with this, when they see what is good, moves towards it; and when they see their errors, they turn from them.

Yi indicates that in the state which it denotes there will be advantage in every movement which shall be undertaken, that it will be advantageous even to cross the great stream.
""",
                1:"""nine: shows that it will be advantageous for its subject in their position to make a great movement. If it be greatly fortunate, no blame will be imputed to them.""",
                2:"""six: shows parties adding to the stores of its subject ten pairs of tortoise shells whose oracles cannot be opposed. Let them persevere in being firm and correct, and there will be good fortune. Let the king, having their virtues thus distinguished, employ them in presenting their offerings to the supreme being, and there will be good fortune.""",
                3:"""six: shows increase given to its subject by means of what is evil, so that they shall be led to good, and be without blame. Let them be sincere and pursue the path of balance, so shall they secure the recognition of the ruler, like an officer who announces themselves to their prince by the symbol of their rank. """,
                4:"""six: shows its subject pursuing the due course. Their advice to their prince is followed. They can with advantage be relied on in such a movement as that of removing the capital. """,
                5:"""nine: shows its subject with sincere heart seeking to benefit all below. There need be no question about it; the result will be great good fortune. All below will with sincere heart acknowledge their goodness. """,
                6:"""nine: we see one to whose increase none will contribute, while persons will seek to assail them. They observe no regular rule in the ordering of their heart. There will be evil."""
})

def in43data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id43data()",
                'title':""" 43. Kouai / Resolution""", 
                'text':"""
The trigram representing heaven, and that for the waters of a marsh mounting above it, form Kouai. The superior person, in accordance with this, bestows emoluments on those below them, and dislike allowing their gifts to accumulate undispensed.

Kouai requires in those who would fulfil its meaning the exhibition of the culprit's guilt in the royal court, and a sincere and earnest appeal for sympathy and support, with a consciousness of the peril involved in cutting off the criminal. They should also make announcement in their own city, and show that it will not be well to have recourse at once to arms. In this way there will be advantage in whatever they shall proceed with.
""",
                1:"""nine: shows its subject in the pride of strength advancing with their toes. They go forward, but will not succeed. There will be ground for blame.""",
                2:"""nine: shows its subject full of apprehension and appealing for sympathy and help. Late at night hostile measures may be taken against them, but they need not they anxious about them.""",
                3:"""nine: shows its subject about to advance with strong and determined looks. There will be evil. The superior person, bent on cutting off the criminal, will walk alone and encounter the rain till they are hated by their proper associates as if they were contaminated by the criminals. In the end there will be no blame against them.""",
                4:"""nine: shows one from whose buttocks the skin has been stripped, and who walks slowly and with difficulty. If they could act like a sheep led after its companions, occasion for repentance would disappear.  But though they hear these words, they will not believe them.""",
                5:"""nine: shows the small men like a bed of weeds, which ought to be uprooted with the utmost determination. If the subject of the line has such determination, their action, in harmony with their central position, will lead to no error or blame. """,
                6:"""six: shows its subject without any helpers on whom to call. Their end will be evil."""
})

def in44data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id44data()",
                'title':""" 44. Keou / Contacting""", 
                'text':"""
The trigram representing wind, and that for the sky above it, form Keou. The sovereign, in accordance with this, delivers their charges, and promulgates their announcements throughout the four quarters of the kingdom.

Keou shows a subordinate who is bold and strong. It will not be good to partner such a subordinate.
""",
                1:"""six: shows how its subject should be kept like a carriage tied and fastened to a metal drag, in which case with firm correctness there will be good fortune. But if they move in any direction, evil will appear. They will be like a lean pig, which is sure to keep jumping about.""",
                2:"""nine: shows its subject with a wallet of fish. There will be no error. But it will not be well to let the subject of the first line go forward to the guests.""",
                3:"""nine: shows one from whose buttocks the skin has been stripped so that they walk with difficulty. The position is perilous, but there will be no great error. """,
                4:"""nine: shows its subject with their fish wallet, but no fish in it. This will give rise to evil. """,
                5:"""nine: shows a medlar tree overspreading the gourd beneath it. If they keep their brilliant qualities concealed, a good issue will descend as from Heaven.""",
                6:"""nine: shows its subject receiving others on their horns. There will be occasion for regret, but there will be no error."""
})

def in45data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id45data()",
                'title':""" 45. Ts'ouei / The Gathering""", 
                'text':"""
The trigram representing the earth, and that for the waters of a marsh raised above it, form Ts'ouei. The superior person, in accordance with this, has their weapons of war put in good repair, to be prepared against unforeseen contingencies.

In the state denoted by Ts'ouei, the king will repair to their ancestral temple. It will be advantageous also to meet with the great person; and then there will be progress and success, though the advantage must come through firm correctness. The use of great victims will conduce to good fortune: and in whatever direction movement is made, it will be advantageous.
""",
                1:"""six: shows its subject with a sincere desire for union, but unable to carry it out, so that disorder is brought into the sphere of their union. If they cry out for help to their proper correlate, all at once their tears will give way to smiles. They need not mind the temporary difficulty; as they go forward, there will be no error.""",
                2:"""six: shows its subject led forward by their correlate. There will be good fortune, and freedom from error. There is complete sincerity, and in that case even the small offerings of the vernal sacrifice are acceptable.""",
                3:"""six: shows its subject striving after union and seeming to sigh, yet nowhere finding any advantage. If they go forward, they will not err, though there may be some small cause for regret. """,
                4:"""nine: shows its subject in such a state that, if they be greatly fortunate, they will receive no blame. """,
                5:"""nine: shows the union of all under its subject in the place of dignity. There will be no error. If any do not have confidence in them, let them see to it that their virtue be great, long-continued, and firmly correct, and all occasion for repentance will disappear. """,
                6:"""six: shows its subject sighing and weeping; but there will be no error."""
})

def in46data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id46data()",
                'title':""" 46. Cheng / Promotion""", 
                'text':"""
The trigram representing wood, and that for the earth with the wood growing in the midst of it, form Cheng. The superior person, in accordance with this, pays careful attention to their virtue, and accumulates the small developments of it until it is high and great.

Cheng indicates that under its conditions there will be great progress and success. Seeking by the qualities implied meet with the great person, its subject need have no anxiety. Advance to the south will be fortunate.
""",
                1:"""six: shows its subject advancing upwards with the welcome of those above them. There will be great good fortune.""",
                2:"""nine: shows its subject with that sincerity which will make even the small offerings of the vernal sacrifice acceptable. There will be no error.""",
                3:"""nine: shows its subject ascending upwards as into an empty city.""",
                4:"""six: shows its subject employed by the king to present their offerings on the mountain. There will be good fortune; there will be no mistake. """,
                5:"""six: shows its subject firmly correct, and therefore enjoying good fortune. They ascend the stairs with all due ceremony. """,
                6:"""six: shows its subject advancing upwards blindly. Advantage will be found in a ceaseless maintenance of firm correctness."""
})

def in47data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id47data()",
                'title':""" 47. K'oun / Weariness""", 
                'text':"""
The trigram representing a marsh, and below it for a defile, which has drained the other dry so that there is no water in it, form K'oun. The superior person, in accordance with this, will sacrifice their life in order to carry out their purpose.

In the condition denoted by K'oun there may yet be progress and success. For the firm and correct, the really great person, there will be good fortune. They will fall into no error. If they make speeches, their words cannot be made good.
""",
                1:"""six: shows its subject with their buttocks straitened under the stump of a tree. They enter a dark valley, and for three years have no prospect of deliverance.""",
                2:"""nine: shows its subject straitened amidst their wine and viands. There come to them anon the red knee-covers of the ruler. It will be well for them to maintain their sincerity as in sacrificing. Active operations on their part will lead to evil, but they will be free from blame.""",
                3:"""six: shows its subject straitened before a frowning rock. They lay hold of thorns. They enter their palace, and do not see their spouse. There will be evil.""",
                4:"""nine: shows its subject proceeding very slowly to help the subject of the first line, who is straitened by the carriage adorned with metal in front of them. There will be occasion for regret, but the end will be good. """,
                5:"""nine: shows its subject with their nose and feet cut off. They are straitened by their ministers in their scarlet aprons. They are leisurely in their movements, however, and are satisfied. It will be well for them to be as sincere as in sacrificing to spiritual beings. """,
                6:"""six: shows its subject straitened, as if bound with creepers; or in a high and dangerous position, and saying to themselves,  'If  I move, I shall repent it.' If they do repent of former errors, there will be good fortune in their going forward."""
})

def in48data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id48data()",
                'title':""" 48. Tsing / A Well""", 
                'text':"""
The trigram representing wood, and above it that for water, form Tsing. The superior person, in accordance with this, comforts the people, and stimulates them to mutual helpfulness.

Looking at Tsing, we think of how the site of a town may be changed, while the fashion of its wells undergoes no changes. The water of a well never disappears and never receives any great increase, and those who come and those who go can draw and enjoy the benefit. If the drawing has nearly been accomplished, but, before the rope has quite reached the water, the bucket is broken, this is evil.
""",
                1:"""six: shows a well so muddy that people will not drink of it; or an old well to which neither birds nor other creatures resort.""",
                2:"""nine: shows a well from which by a hole the water escapes and flows away to the shrimps and such small creatures among the grass, or one the water of which leaks away as from a broken basket.""",
                3:"""nine: shows a well, which has been cleared out, but is not used. Our hearts are sorry for this, for the water might be drawn out and used. If the king were only intelligent, both they and we might receive the benefit of it. """,
                4:"""six: shows a well, the lining of which is well laid. There will be no error. """,
                5:"""nine: shows a clear, limpid well, the waters from whose cold spring are freely drunk.""",
                6:"""six: shows the water from the well brought to the top, which is not allowed to be covered. This suggests the idea of sincerity. There will be great good fortune."""
})

def in49data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id49data()",
                'title':""" 49. Keu / The Revolution""", 
                'text':"""
The trigram representing the waters of a marsh, and that for fire in the midst of them, form Keu. The superior person, in accordance with this, regulates their astronomical calculations, and makes clear the seasons and times.

What takes place as indicated by Keu is believed in only after it has been accomplished. There will be great progress and success. Advantage will come from being firm and correct. In that case occasion for repentance will disappear.
""",
                1:"""nine: shows its subject as if they were bound with the skin of a yellow ox.""",
                2:"""six: shows its subject making their changes after some time has passed. Action taken will be fortunate There will be no error.""",
                3:"""nine: shows that action taken by its subject will be evil. Though they be firm and correct, their position is perilous. If the changes he contemplates have been three times fully discussed, they will be believed in. """,
                4:"""nine: shows occasion for repentance disappearing from its subject. Let them be believed in; and though they change existing ordinances, there will be good fortune. """,
                5:"""nine: shows the great person producing their changes as the tiger does when it changes its stripes. Before they divine and proceed to action, faith has been reposed in them. """,
                6:"""six: shows the superior person producing their changes as the leopard does when it changes its spots, while small people change their faces and show their obedience. To go forward now would lead to evil, but there will be good fortune in abiding in the firm and correct."""
})

def in50data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id50data()",
                'title':""" 50. Ting / The Cauldron""", 
                'text':"""
The trigram representing wood, and above it that for fire, form Ting. The superior person, in accordance with this, keeps their every position correct, and maintains secure the appointment of Heaven.

Ting gives the intimation of great progress and success.
""",
                1:"""six: shows the caldron overthrown and its feet turned up, but there will be advantage in its getting rid of what was in it. Or it shows us the concubine whose position is improved by means of her son. There will be no error.""",
                2:"""nine: shows the caldron with the things to be cooked in it. If its subject can say, 'My enemy dislikes me, but they cannot approach me', there will be good fortune.""",
                3:"""nine: shows the caldron with the places of its handles changed. The progress of its subject is thus stopped. The flesh of the pheasant which is in the caldron with not be eaten. But the genial rain will come, and the grounds for repentance will disappear. There will be good fortune in the end. """,
                4:"""nine: shows the caldron with its feet broken; and its contents, designed for the ruler's use, overturned and spilt. Its subject will be made to blush for shame. There will be evil. """,
                5:"""six: shows the caldron with yellow ears and rings of metal in them. There will be advantage through being firm and correct. """,
                6:"""nine: shows the caldron with rings of jade. There will be great good fortune, and all action taken will be in every way advantageous."""
})

def in51data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id51data()",
                'title':""" 51. Tchen / The Thunder""", 
                'text':"""
The trigram representing thunder, being repeated, forms Tchen. The superior person, in accordance with this, is fearful and apprehensive, cultivates their virtues, and examines their faults.

Tchen gives the intimation of ease and development. When the time of movement which it indicates comes, the subject of the hexagram will be found looking out with apprehension, and yet smiling and talking cheerfully. When the movement like a crash of thunder terrifies all within a hundred miles, they will be like the sincere worshipper who is not startled into letting go their ladle and cup of sacrificial spirits.
""",
                1:"""nine: shows its subject, when the movement approaches, looking out and around with apprehension, and afterwards smiling and talking cheerfully. There will be good fortune.""",
                2:"""six: shows its subject, when the movement approaches, in a position of peril. They judge it better to let go the articles in their possession, and to ascend a very lofty height. There is no occasion for them to pursue after the things they have let go; in seven days they will find them.""",
                3:"""six: shows its subject distraught amid the startling movements going on. If those movements excite them to right action, there will be no mistake. """,
                4:"""nine: shows its subject amid the startling movements, supinely sinking deeper in the mud. """,
                5:"""six: shows its subject going and coming amidst the startling movements of the time, and always in peril, but perhaps they will not incur loss, and find business which they can accomplish. """,
                6:"""six: shows its subject, amidst the startling movements of the time, in breathless dismay and looking round them with trembling apprehension. If they take action, there will be evil. If, while the startling movements have not reached their own person and their neighbourhood, they were to take precautions, there would be no error, but their relatives might still speak against them."""
})

def in52data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id52data()",
                'title':""" 52. Ken / The Stilling, The Mountain""", 
                'text':"""
Two trigrams representing a mountain, one over the other, form Ken. The superior person, in accordance with this, does not go in their thoughts beyond the duties of the position in which they are.

When one's resting is like that of the back, and they lose all consciousness of self; when they walk in their courtyard, and do not see any of the persons in it, there will be no error.
""",
                1:"""six: shows its subject keeping their toes at rest. There will be no error; but it will be advantageous for them to be persistently firm and correct""",
                2:"""six: shows its subject keeping the calves of their legs at rest. They cannot help the subject of the line above whom they follow, and are dissatisfied in their mind.""",
                3:"""nine: shows its subject keeping their loins at rest, and separating the ribs from the body below. The situation is perilous, and the heart glows with suppressed excitement. """,
                4:"""six: shows its subject keeping their trunk at rest. There will be no error.""",
                5:"""six: shows its subject keeping their jawbones at rest, so that their words are all orderly. Occasion for repentance will disappear. """,
                6:"""nine: shows its subject devotedly maintaining their restfulness. There will be good fortune."""
})

def in53data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id53data()",
                'title':""" 53. Tchien / Gradual Progress""", 
                'text':"""
The trigram representing a mountain, and above it that for a tree, form Tchien. The superior person, in accordance with this, attains to and maintains their extraordinary virtue, and makes the manners of the people good.

Tchien suggest to us the marriage of a young lady, and the good fortune attending it. There will be advantage in being firm and correct.
""",
                1:"""six: shows the wild geese gradually approaching the shore. A young officer in similar circumstances will be in a position of danger, and be spoken against; but there will be no error.""",
                2:"""six: shows the geese gradually approaching the large rocks, where they eat and drink joyfully and at ease. There will be good fortune.""",
                3:"""nine: shows them gradually advanced to the dry plains. It suggests also the idea of a husband who goes on an expedition from which he does not return, and of a wife who is pregnant, but will not nourish her child. There will be evil. The case symbolised might be advantageous in resisting plunderers. """,
                4:"""six: shows the geese gradually advanced to the trees. They may light on the flat branches. There will be no error. """,
                5:"""nine: shows the geese gradually advanced to a high mound. It suggests the idea of a wife who for three years does not become pregnant; but in the end the natural issue cannot they prevented. There will be good fortune. """,
                6:"""nine: shows the geese gradually advanced to the large heights beyond. Their feathers can be used as ornaments. There will be good fortune."""
})

def in54data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id54data()",
                'title':""" 54. Kouei Mei / The Marriageable Maiden""", 
                'text':"""
The trigram representing the waters of a marsh, and over it that for thunder, form Kouei Mei. The superior person, in accordance with this, having regard to the far distant end, knows the mischief that may be done at the beginning.

Kouei Mei indicates that under the conditions which it denotes action will be evil, and in no wise advantageous.
""",
                1:"""nine: shows the younger sister married off in a position ancillary to the real wife. It suggests the idea of a person lame on one leg who yet manages to tramp along. Going forward will be fortunate.""",
                2:"""nine: shows her blind of one eye, and yet able to see. There will be advantage in her maintaining the firm correctness of a solitary widow.""",
                3:"""six: shows the younger sister who was to be married off in a mean position. She returns and accepts an ancillary position. """,
                4:"""nine: shows the younger sister who is to be married off protracting the time. She may be late in being married, but the time will come.""",
                5:"""six: reminds us of the marrying of the younger sister of the king, when the sleeves of the princess were not equal to those of the still younger sister who accompanied her in an inferior capacity. The case suggests the thought of the moon almost full. There will be good fortune. """,
                6:"""six: shows the young lady bearing the basket, but without anything in it, and the gentleman slaughtering the sheep, but without blood flowing from it. There will be no advantage in any way."""
})

def in55data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id55data()",
                'title':""" 55. Fong / Abundance, Fullness""", 
                'text':"""
The trigrams representing thunder and lightning combine to form Fong. The superior person, in accordance with this, decides cases of litigation, and apportions punishments with exactness.

Fong intimates progress and development. When a king has reached the point which the name denotes, there is no occasion to be anxious through fear of change. Let them be as the sun at noon.
""",
                1:"""nine: shows its subject meeting with their mate. Though they are both of the same character, there will be no error. Advance will call forth approval.""",
                2:"""six: shows its subject surrounded by screens so large and thick that at midday they can see from them the constellation of the Bushel. If they go and try to enlighten their ruler who is thus emblemed, they will make themselves to be viewed with suspicion and dislike. Let them cherish their feeling of sincere devotion that they may thereby move their ruler's mind, and there will be good fortune.""",
                3:"""nine: shows its subject with an additional screen of a large and thick banner, through which at midday they can see the small Mei star. In the darkness they break their right arm; but there will be no error. """,
                4:"""nine: shows its subject in a tent so large and thick that at midday they can see from it the constellation of the Bushel. But they meet with the subject of the first line, as nine like themselves. There will be good fortune. """,
                5:"""six: shows its subject bringing around them people of brilliant ability. There will be occasion for congratulation and praise. There will be good fortune.""",
                6:"""six: shows its subject with their house made large, but only serving as a screen to their household. When they look at their door, it is still, and there is nobody about it. For three years no one is to be seen. There will be evil."""
})

def in56data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id56data()",
                'title':""" 56. Lu / The Traveler""", 
                'text':"""
The trigram representing a mountain, and above it that for fire, form Lu. The superior person, in accordance with this, exerts their wisdom and caution in the use of punishments and in not allowing litigations to continue.

Lu intimates that in the condition which it denotes there may be some little attainment and progress. If the stranger or traveller be firm and correct as they ought to be, there will be good fortune.
""",
                1:"""six: shows the stranger mean and meanly occupied. It is thus that they bring on themselves further calamity.""",
                2:"""six: shows the stranger, occupying their lodging-house, carrying with them their means of livelihood, and provided with good and trusty servants.""",
                3:"""nine: shows the stranger burning their lodging-house, and having lost their servants. However firm and correct they try to be, they will be in peril.""",
                4:"""nine: shows the traveller in a resting-place, having also the means of livelihood and the axe, but still saying, ' I am not at ease in my mind.' """,
                5:"""six: shows its subject shooting a pheasant. They will lose their arrow, but in the end they will obtain praise and a high charge. """,
                6:"""nine: suggests the idea of a bird burning its nest. The stranger, thus represented, first laughs and then cries out. They have lost their ox-like docility too readily and easily. There will be evil."""
})

def in57data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id57data()",
                'title':""" 57. Hsuan / Willing Submission, The Wind""", 
                'text':"""
The two trigrams representing wind, following each other, form Hsuan. The superior person, in accordance with this, reiterates their orders, and secures the practice of their affairs.

Hsuan intimates that under the conditions which it denotes there will be some little attainment and progress. There will be advantage in movement onward in whatever direction. It will be advantageous also to see the great person.
""",
                1:"""six: shows its subject now advancing, now receding. It would be advantageous for them to have the firm correctness of a brave soldier.""",
                2:"""nine: shows the representative of Hsuan beneath a couch, and employing diviners and exorcists in a way bordering on confusion. There will be good fortune and no error.""",
                3:"""nine: shows its subject penetrating only by violent and repeated efforts, There will be occasion for regret. """,
                4:"""six: shows all occasion for repentance in its subject passed away. They take game for its threefold use in their hunting. """,
                5:"""nine: shows that with firm correctness there will be good fortune for its subject. All occasion for repentance will disappear, and all their movements will be advantageous. There may have been no good beginning, but there will be a good end. Three days before making any changes, let them give notice of them; and three days after, let them reconsider them. There will thus be good fortune. """,
                6:"""nine: shows the representative of Hsuan beneath a couch, and having lost the axe with which they executed their decisions. However firm and correct they may try to they, there will be evil."""
})

def in58data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id58data()",
                'title':""" 58. Touei / Happyness, The Lake""", 
                'text':"""
Two symbols representing the waters of a marsh, one over the other, form Touei. The superior person, in accordance with this, encourages the conversation of friends and the stimulus of their common practice.

Touei intimates that under its conditions there will be progress and attainment, but it will be advantageous to be firm and correct.
""",
                1:"""nine: shows the pleasure of inward harmony. There will be good fortune.""",
                2:"""nine: shows the pleasure arising from inward sincerity. There will be good fortune. Occasion for repentance will disappear.""",
                3:"""six: shows its subject bringing round themselves whatever can give pleasure. There will be evil. """,
                4:"""nine: shows its subject deliberating about what to seek their pleasure in, and not at rest. They border on what would be injurious, but there will be cause for joy. """,
                5:"""nine: shows its subject trusting in one who would injure them. The situation is perilous. """,
                6:"""six: shows the pleasure of its subject in leading and attracting others."""
})

def in59data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id59data()",
                'title':""" 59. Houan / The Dissolution, The Scattering""", 
                'text':"""
The trigram representing water, and that for wind moving above the water, form Houan. The ancient kings, in accordance with this, presented offerings to the deity and established the ancestral temple.

Houan intimates that under its conditions there will be progress and success. The king goes to their ancestral temple; and it will be advantageous to cross the great stream. It will be advantageous to be firm and correct.
""",
                1:"""six: shows its subject engaged in rescuing from the impending evil, and having the assistance of a strong horse. There will be good fortune.""",
                2:"""nine: shows its subject, amid the dispersion, hurrying to their contrivance for security. All occasion for repentance will disappear.""",
                3:"""six: shows its subject discarding any regard to their own person. There will be no occasion for repentance. """,
                4:"""six: shows its subject scattering the different parties in the the state; which leads to great good fortune. From the dispersion they collect again good people standing out, a crowd like a mound, which is what ordinary folk would not have thought of. """,
                5:"""nine: shows its subject amidst the dispersion issuing their great announcements as the perspiration flows from their body. They scatter abroad also the accumulation in the royal granaries. There will be no error. """,
                6:"""nine: shows its subject disposing of what may be called its bloody wounds, and going and separating themselves from their anxious fears. There will be no error."""
})

def in60data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id60data()",
                'title':""" 60. Tchieh / Limitation""", 
                'text':"""
The trigram representing a lake, and above it that for water, form Tchieh. The superior person, in accordance with this, constructs their methods of numbering and measurement, and discusses points of virtue and conduct.

Tchieh intimates that under its conditions there will be progress and attainment. But if the regulations which it prescribes be severe and difficult, they cannot be permanent.
""",
                1:"""nine: shows its subject not quitting the courtyard outside their door. There will be no error.""",
                2:"""nine: shows its subject not quitting the courtyard inside their gate. There will be evil.""",
                3:"""six: shows its subject with no appearance of observing the proper regulations, in which case we shall see them lamenting. But there will be no one to blame but themselves. """,
                4:"""six: shows its subject quietly and naturally attentive to all regulations. There will be progress and success. """,
                5:"""nine: shows its subject sweetly and acceptably enacting their regulations. There will be good fortune. Their onward progress will afford grounds for admiration. """,
                6:"""six: shows its subject enacting regulations severe and difficult. Even with Firmness and correctness there will be evil. But though there will be cause for repentance, it will by and by disappear."""
})

def in61data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id61data()",
                'title':""" 61. Tchong Fou / The Interior Truth""", 
                'text':"""
The trigram representing the waters of a marsh, and that for wind above it, form Tchong Fou. The superior person, in accordance with this, deliberates about causes of litigations and delays the infliction of death.

Tchong Fou moves even pigs and fish, and leads to good fortune. There will be advantage in crossing the great stream. There will be advantage in being firm and correct.
""",
                1:"""nine: shows its subject resting in their self. There will be good fortune. If they sought to rest in any other, they would not find rest.""",
                2:"""nine: shows its subject like the crane crying out in her hidden retirement, and her young ones responding to her. It is as if it were said, 'I have a cup of good spirits', and the response were, 'I will partake of it with you.' """,
                3:"""six: shows its subject having met with their mate. Now they beat their drum, and now they leave off. Now they weep, and now they sing. """,
                4:"""six: shows its subject like the moon nearly full, and like a horse in a chariot whose fellow disappears. There will be no error. """,
                5:"""nine: shows its subject perfectly sincere, and linking others to them in closest union. There will be no error. """,
                6:"""nine: shows its subject on a rooster trying to mount to heaven. Even with firm correctness there will be evil."""
})

def in62data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id62data()",
                'title':""" 62. Siao Kouo / The Small Get By""", 
                'text':"""
The trigram representing a hill, and that for thunder above it, form Siao Kouo. The superior person, in accordance with this, in their conduct exceeds in humility, in mourning exceeds in sorrow, and their expenditure exceeds in economy.

Siao Kouo indicates that in the circumstances which it implies there will be progress and attainment, but it will be advantageous to be firm and correct. What it denotes may be done in small affairs, but not in great affairs. It is like the notes that come down from a bird on the wing; to descend is better than to ascend. There will in this way be great good fortune.
""",
                1:"""six: suggests the idea of a bird flying, and ascending till the issue is evil.""",
                2:"""six: shows its subject passing by their grandfather, and meeting with their grandmother; not attempting anything against their ruler, but meeting them as their minister. There will be no error.""",
                3:"""nine: shows its subject taking no extraordinary precautions against danger; and some in consequence finding opportunity to assail and injure them. There will be evil. """,
                4:"""nine: shows its subject falling into no error, but meeting the exigency of their situation, without exceeding in their natural course. If they go forward, there will be peril, and they must they cautious. There is no occasion for their using firmness perpetually. """,
                5:"""six: suggests the idea of being in the west. It also shows the prince shooting their arrow, and taking the bird in a cave. """,
                6:"""six: shows its subject not meeting the exigency of their situation, and exceeding their proper course. It suggests the idea of a bird flying far aloft. There will be evil. The case is one of calamity and self-produced injury."""
})

def in63data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id63data()",
                'title':""" 63. Tchi Tchi / After The Achievement""", 
                'text':"""
The trigram representing fire, and that for water above it, form Tchi Tchi. The superior person, in accordance with this, thinks of evil that may come, and beforehand guards against it.

Tchi Tchi intimates progress and success in small matters. There will be advantage in being firm and correct. There has been good fortune in the beginning; there may be disorder in the end.
""",
                1:"""nine: shows as a driver who drags back their wheel, or as a fox which has wet their tail. There will be no error.""",
                2:"""six: shows as a wife who has lost her carriage-screen. There is no occasion to go in pursuit of it. In seven days she will find it. """,
                3:"""nine: suggests the case of Ko Chung who attacked the Demon region, but was three years in subduing it. Small men should not be employed in such enterprises. """,
                4:"""six: shows its subject with rags provided against any leak in their boat, and on their guard all day long. """,
                5:"""nine: shows  the neighbour in the east who slaughters an ox for their sacrifice; but this is not equal to the small spring sacrifice of the neighbour in the west, whose sincerity receives the blessing. """,
                6:"""six: shows its subject with even their head immersed. The position is perilous."""
})

def in64data() -> str:
        return BuildHtml({ 'imgSrc':"pyching_idimage_data.id64data()",
                'title':""" 64. Wei Tchi / Before The Achievement""", 
                'text':"""
The trigram representing water, and that for fire above it, form Wei Tchi. The superior person, in accordance with this, carefully discriminates among the qualities of things, and the different positions they naturally occupy.

Wei Tchi intimates progress and success in the circumstances which it implies. We see a young fox that has nearly crossed the stream, when its tail gets immersed. There will be no advantage in any way.
""",
                1:"""six: shows its subject with occasion for regret.""",
                2:"""nine: shows its subject dragging back their carriage-wheel. With firmness and correctness there will be good fortune.""",
                3:"""six: shows its subject, with the state of things not yet remedied, advancing on; which will lead to evil. But there will be advantage in trying to cross the great stream. """,
                4:"""nine: shows its subject by firm correctness obtaining good fortune, so that all occasion for repentance disappears. Let them stir themselves up, as if they were invading the Demon region, where for three years rewards will come to them and their troops from the great kingdom. """,
                5:"""six: shows its subject by firm correctness obtaining good fortune, and having no occasion for repentance. We see in them the brightness of a superior person, and the possession of sincerity. There will be good fortune. """,
                6:"""nine: shows its subject full of confidence and therefore feasting quietly. There will be no error. But if they cherish this confidence, till they are like the fox who gets their head immersed, it will fail of what is right."""
})

### end of module
