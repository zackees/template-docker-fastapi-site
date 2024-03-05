# media-bias-scorer

# Brief

This is to be a fastapi app. All of what I'm going to describe has already been a pattern being used for the AmericasDigitalShield site. Please refer to that.

The app will have the following endpoints:

  * POST /api/youtube/channel
    * Header: Auth token (just make up a sufficiently large random token)
    * body: the channel id
    * returns: a json response
      * ok: { ok: True, rank: float, err: None }
      * not found: { ok: Fale, rank: None, err: "Not Found" }
  * POST /api/youtube/video
    * Header: Autho token
    * body: the video id (for example ?watch=XXXX where XXXX is the video id)
    * returns: a josn response
      * ok: { ok: True, rank: float, channel_id: str, err: None }
      * not found: { ok: False, rank: None, channel_id: None, err: "Not Found" }


## Endpoint management:

  * All endpoints will input pydantic objects, and return pydantic objects.
    * Pydantic models convert to json for input and outputs, and are type checked
    * They will also become part of the openapi that's automatically generated for the fastapi site


## Database

  * Use the postgres database in render.com
  * Use the sqlaclchemy ORM to model and access the postgres

  * Models.py will model the postgres database
  * db.py will use models.py to query, and return data as a pydantic object that will be returned
  * It's important to note that the api endpoints should be as simple as possible, with db.py doing most of the work.


## Background worker

  * A background worker will perioidically scrape youtube and collect data on all videos to target channels. We will use yt-dlp for this task.
  * But don't worry too much about how this is scheduled.


# First deliverables

  * Generate all the boilerplate listed in this document and then contact me for next steps.
