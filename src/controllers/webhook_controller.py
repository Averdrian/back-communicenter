import os


class WebhookController:

    def verify(verify_args):
        if verify_args['mode'] == 'subscribe' and verify_args['verify_token'] == os.getenv('WA_VERIFY_TOKEN'):
            return verify_args['challenge'], 200
        else: return { 'error' : "could not verify"}, 400