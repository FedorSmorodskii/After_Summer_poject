from fastapi import APIRouter

router = APIRouter(prefix='/items')


@router.get("/")
def list_items():
    return {
        'item1',
        'item2'
    }


@router.get(f'/{"item_id"}/')
def item_by_id(item_id: int):
    return {
        'item': 'some_item',
        'id': item_id
    }
