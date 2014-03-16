## Rich Meier
## Graphing Utility for UCT ALGORITHM RESULTS

import pylab as p

## DATA ######################################################################
xdata = [0.1, 1.,10]
## Data for 8x8
# opp_size = [[black and random],[white and random], [black, greedy default],[white, greedy default]]
R_88 = [[29,39,46],[20,21,41],[26,31,45],[23,32,32]]
G_88 = [[32,39,47],[39,39,42],[44,54,51],[47,46,40]]
M2_88 = [[14,30,56],[44,52,47],[21,28,24],[38,48,48]]
M3_88 = [[9,30,26],[48,48,40],[-1,16,28],[29,36,36]]
M4_88 = [[-2,26,42],[39,42,47],[1,19,30],[51,46,45]]

R_66 = [[20,30,31],[12,21,25],[19,30,31],[15,18,21]]
G_66 = [[25,28,33],[18,29,26],[26,32,27],[23,23,31]]
M2_66 = [[2,22,29],[29,25,29],[2,-3,20],[25,35,30]]
M3_66 = [[18,29,28],[21,26,28],[-7,17,27],[22,26,29]]
M4_66 = [[-18,20,16],[28,30,31],[-8,7,9],[27,30,34]]

## PLOT CONSTANTS ############################################################
indices1 = [0,2.5,5]
indices2 = [.5, 3, 5.5] 
indices3 = [1, 3.5, 6] 
indices4 = [1.5, 4, 6.5] 
barwidth = .5
opponentDict88 = {'Random_Policy':R_88, 'Greedy_Policy':G_88, 'Minimax2':M2_88, 'Minimax3':M3_88, 'Minimax4':M4_88}
opponentDict66 = {'Random_Policy':R_66, 'Greedy_Policy':G_66, 'Minimax2':M2_66, 'Minimax3':M3_66, 'Minimax4':M4_66}

for key in opponentDict66.keys():
    fig, a = p.subplots(figsize=(17,10))
    bars1 = a.bar(indices1, opponentDict66[key][0], width=barwidth, color='k',hatch='|', edgecolor='w')
    bars2 = a.bar(indices2, opponentDict66[key][1], width=barwidth, color='w',hatch='|', label="UCT Default Policy = Random")
    bars3 = a.bar(indices3, opponentDict66[key][2], width=barwidth, color='k',hatch="-", edgecolor='w')
    bars4 = a.bar(indices4, opponentDict66[key][3], width=barwidth, color='w',hatch="-", label="UCT Default Policy = Greedy")

    a.set_xticks((1, 3.5, 6))
    a.set_xticklabels(('0.1', '1', '10'))
    a.set_yticks((-36,-30,-20,-10,0,10,20,30,36))
    a.set_xlim((0,7.55))
    a.set_ylim((-36,36))
    p.title("UCT Performance on 6x6 Grid: Opponent = {0}".format(key), fontsize=24)
    p.xlabel("UCT Thinking Time/Move (s)", fontsize=20)
    p.ylabel("Average Margin of Victory (10 Games)", fontsize=20)
    
    a.axhline(0,color='.5',linewidth=1)
    a.set_axis_bgcolor('g')
    p.legend(loc = 'lower right', handleheight=2.5)
    #p.grid()
    a.yaxis.grid(True, color='.8')
    #p.savefig('66_{0}'.format(key))

for key in opponentDict88.keys():
    fig, a = p.subplots(figsize=(17,10))
    bars1 = a.bar(indices1, opponentDict88[key][0], width=barwidth, color='k',hatch='|', edgecolor='w')
    bars2 = a.bar(indices2, opponentDict88[key][1], width=barwidth, color='w',hatch='|', label="UCT Default Policy = Random")
    bars3 = a.bar(indices3, opponentDict88[key][2], width=barwidth, color='k',hatch="-", edgecolor='w')
    bars4 = a.bar(indices4, opponentDict88[key][3], width=barwidth, color='w',hatch="-", label="UCT Default Policy = Greedy")

    a.set_xticks((1, 3.5, 6))
    a.set_xticklabels(('0.1', '1', '10'))
    a.set_yticks((-64,-60,-50,-40,-30,-20,-10,0,10,20,30,40,50,60,64))
    a.set_xlim((0,7.55))
    a.set_ylim((-64,64))
    p.title("UCT Performance on 8x8 Grid: Opponent = {0}".format(key), fontsize=24)
    p.xlabel("UCT Thinking Time/Move (s)", fontsize=20)
    p.ylabel("Average Margin of Victory (10 Games)", fontsize=20)
    
    a.axhline(0,color='.5',linewidth=1)
    a.set_axis_bgcolor('g')
    p.legend(loc = 'lower right', handleheight=2.5)
    #p.grid()
    a.yaxis.grid(True, color='.8')
    #p.savefig('88_{0}'.format(key))

p.show()







