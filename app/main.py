from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app import db, ml, viz

description = """
Welcome to the Spotfy Song Suggester! Trained on over 160k songs beginning from 1920, our model will 
recommend new music we think you'll love!

Visualize a song's audio features to see how danceable your song is!

All you need is a Spotify song URL!

To use these interactive docs:
- Click on an endpoint below
- Click the **Try it out** button
- Edit the Request body or any parameters
- Click the **Execute** button
- Scroll down to see the Server response Code & Details
"""

app = FastAPI(
    title='Spotify Song Suggestor',
    description=description,
    docs_url='/',
)

app.include_router(db.router, tags=['Database'])
app.include_router(ml.router, tags=['Song Suggester'])
app.include_router(viz.router, tags=['Audio Features Visualization'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app)
