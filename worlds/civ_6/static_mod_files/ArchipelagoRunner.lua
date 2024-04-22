TECHS = {}
TECH_BLOCKER_ID = -1

CIVICS = {}
CIVIC_BLOCKER_ID = -1

function OnTurnBegin()
    print("START OnTurnBegin")
    print("END OnTurnBegin")
end

function Init()
    print("Running Main")
    print("Adding turn begin")
    Events.TurnBegin.Add(OnTurnBegin);

    TECHS = DB.Query("Select * FROM Technologies")

    for key, value in pairs(TECHS) do
        if value.TechnologyType == "TECH_BLOCKER" then
            TECH_BLOCKER_ID = key - 1 -- DB index starts at 1, ids start at 0
        end
    end
    print("__________")
    CIVICS = DB.Query("Select * FROM Civics")
    for key, value in pairs(CIVICS) do
      if value.CivicType == "CIVIC_BLOCKER" then
          CIVIC_BLOCKER_ID = key - 1 -- DB index starts at 1, ids start at 0
      end
    end

    players = Game.GetPlayers()
    for key, player in pairs(players) do
        if player:IsHuman() == false then
          -- AP Civics / Techs start with the blocker id and then are populated after
          print("Granting AP techs/civics for AI Player", key)
          for key, value in pairs(TECHS) do
            id = key -1
            if id >= TECH_BLOCKER_ID then
              player:GetTechs():SetTech(id, true)
            end
          end

          for key, value in pairs(CIVICS) do
            id = key -1
            if id >= CIVIC_BLOCKER_ID then
              player:GetCulture():SetCivic(id, true)
            end
          end
        else
          if player:GetCulture():GetProgressingCivic() == 0 then
            print("Setting human player to first AP civic")
            player:GetCulture():SetProgressingCivic(CIVIC_BLOCKER_ID + 1) -- Game starts player researching code of laws, switch it to the first AP civic
          end
        end
    end

    print("Main Completed")
end

-- Init the script
Init()
