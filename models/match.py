class Match:
    def __init__(self, player_1, player_2, p1_score=0, p2_score=0):
        self.player_1 = player_1
        self.player_2 = player_2
        self._p1_score = p1_score
        self._p2_score = p2_score

    def serialize(self):
        return {
            "player_1": self.player_1,
            "player_2": self.player_2,
            "p1_score": self._p1_score,
            "p2_score": self._p2_score,
        }
    
    def __str__(self):
        return f"{self.player_1}: {self._p1_score} - {self._p2_score} :{self.player_2}"
    

    @property
    def p1_score(self):
        """Using the @property decorator to define a getter and a setter for the p1_score attribute"""
        return self._p1_score
    
    @p1_score.setter
    def p1_score(self, value):
        """Setter for the p1_score attribute"""
        self._p1_score = value
        self.player_1.score += value

    @property
    def p2_score(self):
        """Using the @property decorator to define a getter and a setter for the p2_score attribute"""
        return self._p2_score
    
    @p2_score.setter
    def p2_score(self, value):
        """Setter for the p2_score attribute"""
        self._p2_score = value
        self.player_2.score += value

    