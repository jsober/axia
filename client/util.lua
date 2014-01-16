axia.log_label = {}
axia.log_label[axia.ERROR ] = ' [error]'
axia.log_label[axia.WARN  ] = ' [warn]'
axia.log_label[axia.INFO  ] = ' [info]'
axia.log_label[axia.DEBUG ] = ' [debug]'
axia.log_label[axia.DATA  ] = ''

function axia:Log(level, message, args)
    if level ~= axia.DATA and level > axia.log_level then
        return
    end

    local msg = message
    if args then
        print("ARGS:", spickle(args))
        msg = string.format(msg, unpack(args))
    end

    print(string.format('[axia]%s %s', axia.log_label[level], msg))
end

--[[
--
-- Performs an API request to Axia Data Services.
--
--]]
function axia:ApiRequest(api, method, data, on_success, on_error)
    local http  = _HTTP.new()
    local url   = axia.base_url .. api
    http.method = method

    if data ~= nil then
        if method == 'POST' then
            http.POST.add('data', json.encode(data))
        else
            http.GET.add('data', json.encode(data))
        end
    end

    http.urlopen(url, function(response)
        local status  = response.status
        local message = response.statusmsg
        if status ~= 200 then
            axia:Log(axia.ERROR, 'connection error %d: %s', { status, message })
        else
            local json_data = response.body.get()
            local data      = json.decode(json_data)
            if data['result'] == 'success' then
                on_success(data)
            else
                on_error(data)
            end
        end
    end)
end

--[[
--
-- Scans the current sector for anything that could make it a poor choice for
-- navigational purposes, including training sector, stations, bots, and
-- asteroids. Returns true if nothing is found in the sector, false otherwise.
--
--]]
function axia:IsEmptySector()
    local sector_id = GetCurrentSectorid()

    --Always avoid training sectors :)
    if IsTrainingSector(sector_id) then
        return false
    end

    --Detect known bots (hive sectors) and station bots (ergo, stations)   
    if string.find(GetBotSightedInfoForSector(sector_id), 'Bots Sighted:') then
        return false
    end

    local result = true

    --Detect other bots in sector
    ForEachPlayer(function(charid)
        local faction = GetPlayerFaction(charid)
        if faction == 0 then
            result = false
        end
    end)

    --Check for roids in sector
    if result and axia:ScanForAsteroids() then
        result = false
    end

    return result
end

--[[
--
-- Scans the sector for asteroids. Returns true if any are found.
--
--]]
function axia:ScanForAsteroids()
    local seen      = {}
    local obj_id    = 0
    local has_roids = false

    --Store original focus to reset later
    local orig_node_id, orig_obj_id = radar.GetRadarSelectionID()

    --Loop over all targets in the sector, looking for asteroids
    while true do
        gkinterface.GKProcessCommand("RadarNext") 
        local node_id, obj_id = radar.GetRadarSelectionID()

        if obj_id then
            if seen[obj_id] then
                break
            end

            if obj_id and not seen[obj_id] then
                seen[obj_id] = true
                local label, health, dist = GetTargetInfo()

                has_roids = (string.find(label, 'Asteroid'))
                         or (string.find(label, 'Ice Crystal'))

                if has_roids then
                    break
                end
            end
        else
            break
        end
    end

    radar.SetRadarSelection(orig_node_id, orig_obj_id)
    return has_roids
end
