import handlers
from handlers.start import router
from handlers.callback.by_guide import route
from handlers.callback.balance import router
import handlers.callback.no_promo
import handlers.callback.check_promo
import utils.payments.buy
import handlers.callback.viewing_promo
import handlers.callback.viewing_guide
import handlers.callback.withdrawal_balance
import handlers.callback.create_promo
import handlers.type_and_other_message
import handlers.callback.admin_panel


async def include_routers_handlers(dp):
    dp.include_routers(handlers.start.router)
    dp.include_routers(handlers.callback.by_guide.route)
    dp.include_routers(handlers.callback.balance.router)
    dp.include_routers(handlers.callback.no_promo.router)
    dp.include_routers(handlers.callback.check_promo.router)
    dp.include_routers(utils.payments.buy.router)
    dp.include_routers(handlers.callback.viewing_promo.router)
    dp.include_routers(handlers.callback.viewing_guide.router)
    dp.include_routers(handlers.callback.withdrawal_balance.router)
    dp.include_routers(handlers.callback.create_promo.router)

    dp.include_routers(handlers.callback.admin_panel.router)

    dp.include_routers(handlers.type_and_other_message.router)