import time

def start_listeners():
    print("Host => Server is running...")
    time.sleep(2)
    print("Host => Starting event listeners...")

    import modules.scratch
    import modules.tw
    
    time.sleep(1)
    print("Host => Event listeners started and running.")
    
def ping_listeners():
    import modules.scratch
    import modules.tw
    
    while True:
        time.sleep(120)
        try:
            scratch_response = modules.scratch.ping()
            tw_response = modules.tw.ping()
            print(f"Host => Pinged Scratch listener: {scratch_response}")
            time.sleep(2)
            print(f"Host => Pinged TurboWrap listener: {tw_response}")
        except Exception as e:
            print(f"Host => Error pinging listeners: {e}")
    
def start_ping():
    from modules.ping import app
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=6913)

start_listeners()
start_ping()
ping_listeners()