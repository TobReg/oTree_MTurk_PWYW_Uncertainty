from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class GroupWP(WaitPage):

    def after_all_players_arrive(self):
        pass


class Intro(Page):
    def vars_for_template(self):
        return {'treatment': Constants.treatment}
#    pass

# class Instructions(Page):
#    pass


class Question1(Page):
    def vars_for_template(self):
        return {'treatment': Constants.treatment}

    form_model = 'player'
    form_fields = ['question1']

    def error_message(self, values):
        if values['question1'] == 1:
            return "Your answer is not correct. The seller can decide on their own, which pricing mechanism to use."
    pass


class Question2(Page):
    def vars_for_template(self):
        return {'treatment': Constants.treatment}

    form_model = 'player'
    form_fields = ['question2']

    def error_message(self, values):
        if values['question2'] == 1:
            return "Your answer is not correct. If the seller chooses PWYW, the buyers can decide on their own how much to pay for the product."
    pass


class Question3p1(Page):
    def vars_for_template(self):
        return {'treatment': Constants.treatment}

    form_model = 'player'
    form_fields = ['question3s']

    def error_message(self, values):
        if values['question3s'] != -3:
            return "Your answer is not correct. The seller receives no payments but incurs a cost of 3."

    pass


class Question3p2(Page):
    def vars_for_template(self):
        return {'treatment': Constants.treatment}

    form_model = 'player'
    form_fields = ['question3b1']

    def error_message(self, values):
        if values['question3b1'] != 0:
            return "Your answer is not correct. If the buyer does not purchase, there is no consumption and thus no payoff."

    pass


class Question4p1(Page):
    def vars_for_template(self):
        return {'treatment': Constants.treatment}

    form_model = 'player'
    form_fields = ['question4s']

    def error_message(self, values):
        if values['question4s'] != 7:
            return "Your answer is not correct. With two purchases at the price of 5, the seller receives 10 and incurs a cost of 3."

    pass


class Question4p2(Page):
    def vars_for_template(self):
        return {'treatment': Constants.treatment}

    form_model = 'player'
    form_fields = ['question4b1']

    def error_message(self, values):
        if values['question4b1'] != 2:
            return "Your answer is not correct. Buyer 3's payoff is the valuation of 7 minus the price of 5."

    pass


class Question4p3(Page):
    def vars_for_template(self):
        return {'treatment': Constants.treatment}

    form_model = 'player'
    form_fields = ['question4b2']

    def error_message(self, values):
        if values['question4b2'] != -2:
            return "Your answer is not correct. Buyer 2's payoff is the valuation of 3 minus the price of 5."

    pass


class Question5p1(Page):
    def vars_for_template(self):
        return {'treatment': Constants.treatment}

    form_model = 'player'
    form_fields = ['question5b']

    def error_message(self, values):
        if values['question5b'] == 1:
            return "Your answer is not correct. If the seller chooses PWYW and the buyers decide to purchase, then the " \
                   "buyers will know their valuations."

    pass


class Question5p2(Page):
    def vars_for_template(self):
        return {'treatment': Constants.treatment}

    form_model = 'player'
    form_fields = ['question5s']

    def error_message(self, values):
        if values['question5s'] != 6:
            return "Your answer is not correct. Buyers' payments sum to 9 and the seller incurs a cost of 3."

    pass


class QuestionsWP(WaitPage):

    def after_all_players_arrive(self):
        pass


class Role(Page):
    def vars_for_template(self):
        return {'treatment': Constants.treatment}


class MarketInformation(Page):
    def vars_for_template(self):
        return {'treatment': Constants.treatment}
#    pass


class SellerInfoBuyerValuation(Page):

    def vars_for_template(self):
        return {'valuation1': self.player.private_value}
    def is_displayed(self) -> bool:
        return self.player.role() == 'seller' and (Constants.treatment == 1 or Constants.treatment == 2)

class SellerDecisionPricingMechanism(Page):

    form_model = 'group'
    form_fields = ['s_choice_PWYW_FP']

    def is_displayed(self) -> bool:
        return self.player.role() == 'seller'


class SellerDecisionPriceProdCostInfo(Page):

    form_model = 'group'
    form_fields = ['s_decision_price_FP']

    def is_displayed(self) -> bool:
        return self.player.role() == 'seller' and self.group.s_choice_PWYW_FP == 1


class SellerDecisionsWP(WaitPage):

    def after_all_players_arrive(self):
       pass


class BuyerValuationBuyingDecision(Page):

    form_model = 'player'
    form_fields = ['b_decision_buy']

    def vars_for_template(self):
        return {'s_choice': self.group.s_choice_PWYW_FP}
    def is_displayed(self) -> bool:
        return self.player.role() == 'buyer'


class BuyerPriceDecision(Page):

    form_model = 'player'
    form_fields = ['b_decision_price_PWYW']

    def is_displayed(self) -> bool:
        return self.player.role() == 'buyer' and self.group.s_choice_PWYW_FP == 0 and self.player.b_decision_buy == 1


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    pass


class Questionnaire(Page):

    form_model = 'player'
    form_fields = ['survey_easy_difficult', 'survey_risk', 'strategy_seller', 'strategy_buyer', 'age', 'gender', 'feedback']

    pass

class Bye(Page):
    pass

page_sequence = [
    GroupWP,
    Intro,
 #   Instructions,
    Question1,
    Question2,
    Question3p1,
    Question3p2,
    Question4p1,
    Question4p2,
    Question4p3,
    Question5p1,
    Question5p2,
    QuestionsWP,
    Role,
    MarketInformation,
    SellerInfoBuyerValuation,
    SellerDecisionPricingMechanism,
    SellerDecisionPriceProdCostInfo,
    SellerDecisionsWP,
    BuyerValuationBuyingDecision,
    BuyerPriceDecision,
    ResultsWaitPage,
    Results,
    Questionnaire,
    Bye
]
