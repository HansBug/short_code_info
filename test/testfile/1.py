def get_result(self, task_id, path):
    url = 'https://miaohua.sensetime.com/api/v1b/task_result'
    data = {
        "task_id": task_id, # string 任务id
        "token": self.token, # get_token获取的token
    }

    print(f'Generating images for {path}...')
    while True:
        try:
            response = requests.post(url, json=data)
            if json.loads(response.text).get('info').get('state') != 'done':
                time.sleep(5)
                continue
            else:
                break
        except Exception as e:
            print(e)
            time.sleep(5)
            continue
    response = requests.post(url, json=data)
