from databaker.constants import *

def per_file(tableset):
    return "*"

def per_tab(tab):
    obs = tab.excel_ref("A2").assert_one().fill(DOWN).is_not_blank()
    
    tab.col('B').dimension("sale_date", DIRECTLY, RIGHT)
    tab.col('E').dimension("judgement", DIRECTLY, RIGHT)
    tab.col('F').dimension("address", DIRECTLY, RIGHT)
    tab.col('F').filter('City').shift(DOWN).dimension("City", CLOSEST, DOWN)
    tab.col('F').filter('FIRM').shift(DOWN).dimension("Firm", CLOSEST, DOWN)
    '''
    tab.col('A').filter('Status').shift(DOWN).dimension("Status", DIRECTLY, DOWN)
    tab.col('A').filter('Plaintiff').shift(DOWN).dimension("Plaintiff", DIRECTLY, DOWN)
    tab.col('A').filter('Defendant').shift(DOWN).dimension("Defendant", DIRECTLY, DOWN)
    '''

    '''
    tab.excel_ref("A3").fill(RIGHT).is_not_blank().dimension('Broad Industry Group', CLOSEST, LEFT)
    tab.excel_ref("B6").expand(RIGHT).parent().is_not_blank().dimension('AWE Breakdown', DIRECTLY, ABOVE)
    '''
    return obs