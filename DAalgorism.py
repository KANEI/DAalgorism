import copy

class DAalgorism:
    def __init__(self, preference_dict1, preference_dict2):
        self.set_values(preference_dict1, preference_dict2)


    def set_values(self, preference_dict1, preference_dict2):
        """
        初期値を設定する。プレイヤー集合1提案型DAアルゴリズムを考える。
        """
        self.player1 = preference_dict1 #提案可能なプレイヤー集合1の選好を示す辞書
        self.player2 = preference_dict2 #受入可能なプレイヤー集合2の選好を示す辞書

        self.player1_to_reffer = self.player1.copy() #参照用
        self.player1_count = {k:0 for k in list(self.player1.keys())} #提案回数
        self._proposals_dict = {k:[] for k in list(self.player2.keys())} #提案


    def apply_game(self, player_name, i=0):
        """
        player_nameがi番目の選好に応募する。
        i番目の選好が存在しない場合、何もしない。
        """
        if i < len(self.player1[player_name]): 
            preference = self.player1[player_name][i]
            self._proposals_dict[preference].append(player_name)


    def is_over_capacity(self, keep_list, q):
        return len(keep_list) > q


    def remove_least_preferred_player(self, preference_list2, keep_list2):
        """
        選好の低いプレイヤーを1人取り除く。
        """
        for player1 in preference_list2[::-1]:
            if  player1 in keep_list2:
                keep_list2.remove(player1)
                return keep_list2, player1 #取り除いた後の選好と、プレイヤーを返す。


    def choose_player(self, player_name, q):
       """
        プレイヤー2が選好をもとにプレイヤー1を選ぶ。
       """
       preference_list2 = self.player2[player_name]
       keep_list2 = self._proposals_dict[player_name]
       exile_list = []

       while True:
        if self.is_over_capacity(keep_list2, q):
            rlpp = self.remove_least_preferred_player(preference_list2, keep_list2)
            keep_list2 = rlpp[0]
            exile_list.append(rlpp[1])
        else:
            break

        self._proposals_dict[player_name] = keep_list2
        return exile_list


    def filter_players(self, keys_to_keep):
        """
        プレイヤー集合1の辞書から現時点でマッチングしていない人を厳選
        """

        referance_list = self.player1_to_reffer
        new_dict = {key: referance_list[key] for key in keys_to_keep if key in referance_list}
        return new_dict


    def do_step(self, q):

        # プレイヤー1が選考をもとにプレイヤー2に応募する。
        for player1 in list(self.player1.keys()):
            count = self.player1_count[player1]
            self.apply_game(player1,count)

        # プレイヤー2は選考をもとにプレイヤー1を厳選する。
        exiled_list = []
        for player2 in list(self.player2.keys()):
            exiled_players = self.choose_player(player2,q) 
            if exiled_players != None:
                for ep in exiled_players:
                    self.player1_count[ep] += 1
                exiled_list.extend(exiled_players)

        # 提案可能なプレイヤーを更新する。
        self.player1 = self.filter_players(exiled_list)

    def propose_combination(self,q=1):

        # 提案可能なプレイヤーがいなくなるまで繰り返す。
        while len(self.player1) > 0:
            self.do_step(q)

        return self._proposals_dict

    def exchange_players(self,q=1):
        """
        プレイヤー集合2提案型DAメカニズムに変更する。
        """
        self.player1 = self.player2.copy()
        self.player2 = self.player1_to_reffer.copy()

        self.player1_to_reffer = self.player1.copy()
        self.player1_count = {k:0 for k in list(self.player1.keys())}
        self._proposals_dict = {k:[] for k in list(self.player2.keys())}
        return self.propose_combination(q)

if __name__=="__main__":
    dict1 = {"w1":["c1","c2"], "w2":["c2"], "w3":["c2","c1"]}
    dict2 = {"c1":["w3","w2","w1"], "c2":["w1","w2","w3"]}
    da = DAalgorism(dict1,dict2)
    p1 = da.propose_combination(q=2)
    print(p1)

    # もし提案するプレイヤー集合を変更したいなら
    p2 = da.exchange_players(q=2)
    print(p2)



        
        
        


    


    