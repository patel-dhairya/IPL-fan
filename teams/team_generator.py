from models import team
from teams import create_team


def teams():
    gt = team.Team("Gujarat Titans", "GT", "Narendra Modi Stadium")
    gt_url = "https://www.cricbuzz.com/cricket-team/gujarat-titans/971/players"
    gt_players = create_team.create_team(gt_url, gt)

    csk = team.Team("Chennai Super Kings", "CSK", "MA Chidambaram Stadium")
    csk_url = "https://www.cricbuzz.com/cricket-team/chennai-super-kings/58/players"
    csk_players = create_team.create_team(csk_url, csk)

    dc = team.Team("Delhi Capitals", "DC", "Arun Jaitley Stadium")
    dc_url = "https://www.cricbuzz.com/cricket-team/delhi-capitals/61/players"
    dc_players = create_team.create_team(dc_url, dc)

    pbks = team.Team("Punjab Kings", "PBKS", "Punjab Cricket Association IS Bindra Stadium")
    pbks_url = "https://www.cricbuzz.com/cricket-team/punjab-kings/65/players"
    pbks_players = create_team.create_team(pbks_url, pbks)

    kkr = team.Team("Kolkata Knight Riders", "KKR", "Eden Gardens")
    kkr_url = "https://www.cricbuzz.com/cricket-team/kolkata-knight-riders/63/players"
    kkr_players = create_team.create_team(kkr_url, kkr)

    mi = team.Team("Mumbai Indians", "MI", "Wankhede Stadium")
    mi_url = "https://www.cricbuzz.com/cricket-team/mumbai-indians/62/players"
    mi_players = create_team.create_team(mi_url, mi)

    rr = team.Team("Rajasthan Royals", "RR", "Barsapara Cricket Stadium")
    rr_url = "https://www.cricbuzz.com/cricket-team/rajasthan-royals/64/players"
    rr_players = create_team.create_team(rr_url, rr)

    rcb = team.Team("Royal Challengers Bangalore", "RCB", "M.Chinnaswamy Stadium")
    rcb_url = "https://www.cricbuzz.com/cricket-team/royal-challengers-bangalore/59/players"
    rcb_players = create_team.create_team(rcb_url, rcb)

    srh = team.Team("Sunrisers Hyderabad", "SRH", "Rajiv Gandhi International Stadium")
    srh_url = "https://www.cricbuzz.com/cricket-team/sunrisers-hyderabad/255/players"
    srh_players = create_team.create_team(srh_url, srh)

    lsg = team.Team("Lucknow Super Giants", "LSG", "Atal Bihari Vajpayee Ekana Cricket Stadium")
    lsg_url = "https://www.cricbuzz.com/cricket-team/lucknow-super-giants/966/players"
    lsg_players = create_team.create_team(lsg_url, lsg)

    return gt_players + lsg_players + rr_players + mi_players + srh_players + pbks_players + csk_players + rcb_players + \
        dc_players + kkr_players
