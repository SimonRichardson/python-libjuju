"""
This example:

1. Connects to the current model
2. Deploys a charm and waits until it reports itself active
3. Creates an offer
4. Lists the offer
3. Destroys the unit and application

"""
import asyncio

from juju import loop
from juju.controller import Controller
from juju.model import Model


async def main():
    model = Model()
    print('Connecting to model')
    # connect to current model with current user, per Juju CLI
    await model.connect()

    try:
        print('Deploying mysql')
        application = await model.deploy(
            'mysql',
            application_name='mysql',
            series='trusty',
            channel='stable',
        )

        print('Waiting for active')
        await model.block_until(
            lambda: all(unit.workload_status == 'active'
                        for unit in application.units))

        print('Adding offer')
        await model.offer("mysql:db")

        await asyncio.sleep(10)

        print('Removing offer')
        await model.remove_offer("admin/default.mysql", force=True)
    finally:
        print('Disconnecting from model')
        await model.disconnect()


if __name__ == '__main__':
    loop.run(main())
