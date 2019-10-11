from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class GroupWP(WaitPage):

    def after_all_players_arrive(self):
        pass


class Intro(Page):
    pass

class Instructions(Page):
    pass


#class Questions(Page):
#    form_model = 'player'
#    form_fields = ['question1']
#    pass


class QuestionsWP(WaitPage):

    def after_all_players_arrive(self):
        pass


class Role(Page):
    pass


class MarketInformation(Page):
#    def vars_for_template(self):
#        return dict(
#            t=self.group.treatment
#        )
#    def vars_for_template(self):
#        return {'treatment': self.group.treatment}
#    def is_displayed(self):
#        return Constants.treatment == 1 or Constants.treatment == 2

    pass


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
    pass


page_sequence = [
    GroupWP,
    Intro,
    Instructions,
#    Questions,
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
    Questionnaire
]
