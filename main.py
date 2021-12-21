# from websockets import *
import MY_websockets
# create a random string for context ID and reference ID
CONTEXT_ID = MY_websockets.secrets.token_urlsafe(10)
REF_ID = MY_websockets.secrets.token_urlsafe(5)
# copy your (24-hour) token here
TOKEN = 'eyJhbGciOiJFUzI1NiIsIng1dCI6IjhGQzE5Qjc0MzFCNjNFNTVCNjc0M0QwQTc5MjMzNjZCREZGOEI4NTAifQ.eyJvYWEiOiI3Nzc3NSIsImlzcyI6Im9hIiwiYWlkIjoiMTA5IiwidWlkIjoiNEFhfDNIUEk3S3JVeXxuZkxPYUl2dz09IiwiY2lkIjoiNEFhfDNIUEk3S3JVeXxuZkxPYUl2dz09IiwiaXNhIjoiRmFsc2UiLCJ0aWQiOiIyMDAyIiwic2lkIjoiN2U0ZTA4MTliOTBhNDRmMWEyOTBjOTIyMTYxMTRjZmMiLCJkZ2kiOiI4NCIsImV4cCI6IjE2MTg3NjE2MzQifQ.wwCOI5eac7ZCF2T66g8D1zfSdWjTXcQM8BLSlz6dkXkQGtdrFuEwuYqJBfFN2IhhZTYXnki6dDbTKY5ElXC4XQ'

if __name__ == "__main__":

    try:
        print('User starts')
        # MY_websockets.create_subscription(CONTEXT_ID, REF_ID, TOKEN)
        MY_websockets.asyncio.get_event_loop().run_until_complete(MY_websockets.streamer(CONTEXT_ID, REF_ID, TOKEN))
        print ('Can I start a new thread now')
    except KeyboardInterrupt:
        print('User interrupted the interpreter - closing connection.')
        exit()




