import asyncio
import base64
import requests
import cv2
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
import logging

logging.getLogger('ffmpeg').setLevel(logging.ERROR)

# Server URL (replace with your actual server URL)
SERVER_URL = "http://192.168.42.1:8083/stream/s1/channel/0/webrtc?uuid=s1&channel=0"

# Video Display Track
class VideoDisplay(VideoStreamTrack):
    def __init__(self, track):
        super().__init__()
        self.track = track

    async def recv(self):
        frame = await self.track.recv()
        img = frame.to_ndarray(format="bgr24")
        # Do something with the frame, e.g., display or object detection
        cv2.imshow("WebRTC Video", img)
        cv2.waitKey(1)
        return frame

async def main():
    pc = RTCPeerConnection()
    pc.addTransceiver("video", direction="recvonly")

    @pc.on("track")
    def on_track(track):
        if track.kind == "video":
            display = VideoDisplay(track)
            asyncio.ensure_future(display.recv())

    # Create and set local description
    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)

    # Send offer to server
    sdp_offer_base64 = base64.b64encode(pc.localDescription.sdp.encode("utf-8")).decode("utf-8")
    # Prepare headers and data
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
    }
    data = {"data": sdp_offer_base64}

    # Send HTTP POST request
    response = requests.post(SERVER_URL, headers=headers, data=data, verify=False)
    response.raise_for_status()

    # Decode the base64 SDP answer from the server
    sdp_answer = base64.b64decode(response.text).decode("utf-8")

    # Set remote description
    await pc.setRemoteDescription(RTCSessionDescription(sdp=sdp_answer, type="answer"))

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        await pc.close()

if __name__ == "__main__":
    asyncio.run(main())