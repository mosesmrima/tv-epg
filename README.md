# tv-epg

An automatically generated Electronic Program Guide (EPG) for a curated IPTV
playlist. A scheduled GitHub Action runs the [iptv-org/epg](https://github.com/iptv-org/epg)
grabber once a day and publishes an XMLTV guide.

## Guide URL

Use this URL as the EPG source in a player such as TiviMate or Kodi:

```
https://raw.githubusercontent.com/mosesmrima/tv-epg/data/guide.xml.gz
```

The file is a gzip-compressed XMLTV document. Players that accept an EPG URL
decompress it automatically.

## How it works

- `epg.channels.xml` lists the channels to grab. Each entry maps a channel id
  (`xmltv_id`) to an EPG source site and the id of the channel on that site.
  The list was built from the [iptv-org guides API](https://iptv-org.github.io/api/guides.json).
- The workflow in `.github/workflows/epg.yml` clones the iptv-org EPG engine,
  runs the grabber for two days of programs, and force-pushes the result to the
  `data` branch as `guide.xml.gz`. The `data` branch always holds a single
  commit, so the repository stays small.

## Update the channel list

Edit `epg.channels.xml` and commit the change. The next scheduled run, or a
manual run from the Actions tab, picks it up.

## Run it now

Open the Actions tab, select **Generate EPG guide**, and choose **Run workflow**.

## Coverage

Only channels that have a source in the iptv-org guides database get program
data. Channels without a source still appear in the player, but with no guide.
