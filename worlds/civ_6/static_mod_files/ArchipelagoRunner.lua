TECHS = {}
TECH_BLOCKER_ID = -1

CIVICS = {}
CIVIC_BLOCKER_ID = -1
HUMAN_PLAYER = nil

-- Messages read by the client will be started/ended with these
CLIENT_PREFIX = "APSTART:"
CLIENT_POSTFIX = ":APEND"

CHECKED_LOCATIONS = {}

TECH_NOTIFICATION_TYPE = 5
CIVIC_NOTIFICATION_TYPE = 12

-- Sets to true once a turn begins, this is to let the client know that the game can be interacted with now
IS_IN_GAME = false

function OnTurnBegin()
    print("START OnTurnBegin")
    IS_IN_GAME = true
    for key, item in pairs(RECEIVED_ITEMS) do
        GiveItemToPlayer(item, key)
    end
    print("END OnTurnBegin")
end

function NotifyReceivedItem(item, index)
    NotificationManager:SendNotification(NotificationTypes.USER_DEFINED_2, item.Name .. " Received",
        "You have received " .. item.Name .. (item.Sender and " from " .. item.Sender or ""), 0, index) -- 0/index are techincally x/y coords, but if they aren't unique then it won't stack the notifications
end

function GetCheckedLocations()
    print("START GetCheckedLocations")
    locations = {}
    for key, value in pairs(TECHS) do
        id = key - 1
        if id >= TECH_BLOCKER_ID and HUMAN_PLAYER:GetTechs():HasTech(id) then
            table.insert(locations, 1, value.TechnologyType)
        end
    end
    for key, value in pairs(CIVICS) do
        id = key - 1
        if id >= CIVIC_BLOCKER_ID and HUMAN_PLAYER:GetCulture():HasCivic(id) then
            table.insert(locations, 1, value.CivicType)
        end
    end
    print("END GetCheckedLocations")
    return CLIENT_PREFIX .. table.concat(locations, ",") .. CLIENT_POSTFIX
end

function IsInGame()
    result = "true"
    if IS_IN_GAME == false then
        result = "false"
    end
    return CLIENT_PREFIX .. result .. CLIENT_POSTFIX
end

function SetLastReceivedIndex(index)
    Game.SetProperty("LastReceivedIndex", index)
end

function GetLastReceivedIndex()
    return Game.GetProperty("LastReceivedIndex") or -1
end

function ClientGetLastReceivedIndex()
    local index = GetLastReceivedIndex()
    return CLIENT_PREFIX .. tostring(index) .. CLIENT_POSTFIX
end

function HandleReceiveItem(id, name, type, sender)
    print("START HandleReceiveItem type: " .. type)
    received = false
    notification_id = id
    if type == "TECH" and HUMAN_PLAYER:GetTechs():HasTech(id) == false then
        print("Received Tech", id)
        HUMAN_PLAYER:GetTechs():SetResearchProgress(id, 999999)
        received = true

    elseif type == "CIVIC" and HUMAN_PLAYER:GetCulture():HasCivic(id) == false then
        print("Received Civic", id)
        HUMAN_PLAYER:GetCulture():SetCulturalProgress(id, 999999)
        notification_id = id + 100 -- Tech ids and notification ids are not unique between each other
        received = true
    end
    if received then
        SetLastReceivedIndex(GetLastReceivedIndex() + 1)
        NotifyReceivedItem({
            Name = name,
            Sender = sender
        }, notification_id)
        NotifyReceivedItem({
            Name = name,
            Sender = sender
        }, notification_id)
    end

    print("END HandleReceiveItem")
end

function Init()
    print("Running Main")
    print("Adding turn begin")
    -- Events to listen for
    Events.TurnBegin.Add(OnTurnBegin);

    -- Functions to expose to the client
    Game.ReceiveItem = ReceiveItem
    Game.GetCheckedLocations = GetCheckedLocations
    Game.IsInGame = IsInGame
    Game.ClientGetLastReceivedIndex = ClientGetLastReceivedIndex
    Game.SetLastReceivedIndex = SetLastReceivedIndex

    -- Initialize the techs
    TECHS = DB.Query("Select * FROM Technologies")

    for key, value in pairs(TECHS) do
        if value.TechnologyType == "TECH_BLOCKER" then
            TECH_BLOCKER_ID = key - 1 -- DB index starts at 1, ids start at 0
        end
    end
    -- Initialize civics
    CIVICS = DB.Query("Select * FROM Civics")
    for key, value in pairs(CIVICS) do
        if value.CivicType == "CIVIC_BLOCKER" then
            CIVIC_BLOCKER_ID = key - 1 -- DB index starts at 1, ids start at 0
        end
    end

    PLAYERS = Game.GetPlayers()
    for key, player in pairs(PLAYERS) do
        if player:IsHuman() == false then
            -- AP Civics / Techs start with the blocker id and then are populated after
            print("Granting AP techs/civics for AI Player", key)
            for key, value in pairs(TECHS) do
                id = key - 1
                if id >= TECH_BLOCKER_ID then
                    player:GetTechs():SetTech(id, true)
                end
            end

            for key, value in pairs(CIVICS) do
                id = key - 1
                if id >= CIVIC_BLOCKER_ID then
                    player:GetCulture():SetCivic(id, true)
                end
            end
        else
            HUMAN_PLAYER = player
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

Game.HandleReceiveItem = HandleReceiveItem