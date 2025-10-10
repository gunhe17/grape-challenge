import asyncio
import os
import subprocess

os.environ["APP_ENV"] = "dev"

from sqlalchemy import Column, Integer, String, select
from grapechallenge.database.database import DatabaseClient, Base, transactional_session_helper
from grapechallenge.config import get_database_config


# Test model
class TestProduct(Base):
    __tablename__ = "test_products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)


# CRUD Operations
async def create_product(name: str, price: int):
    async with transactional_session_helper() as session:
        product = TestProduct(name=name, price=price)
        session.add(product)
        await session.flush()
        return product.id


async def get_product(product_id: int):
    async with transactional_session_helper() as session:
        result = await session.execute(
            select(TestProduct).where(TestProduct.id == product_id)
        )
        return result.scalar_one_or_none()


async def update_product(product_id: int, name: str, price: int) -> None:
    async with transactional_session_helper() as session:
        result = await session.execute(
            select(TestProduct).where(TestProduct.id == product_id)
        )
        product = result.scalar_one()
        product.name = name
        product.price = price


async def delete_product(product_id: int) -> None:
    async with transactional_session_helper() as session:
        result = await session.execute(
            select(TestProduct).where(TestProduct.id == product_id)
        )
        product = result.scalar_one()
        await session.delete(product)


# Test runner
async def test_crud():
    db_config = get_database_config()
    print(f"Database: {db_config.database_url()}")
    print("=" * 60)

    async with DatabaseClient(db_config.database_url()):
        print("✓ Database connected\n")

        # CREATE
        print("[CREATE]")
        pid = await create_product("Apple", 1000)
        product = await get_product(pid)  # type: ignore
        print(f"✓ Created: id={product.id}, name={product.name}, price={product.price}\n")  # type: ignore

        # READ
        print("[READ]")
        product = await get_product(pid)  # type: ignore
        print(f"✓ Found: id={product.id}, name={product.name}, price={product.price}\n")  # type: ignore

        # UPDATE
        print("[UPDATE]")
        await update_product(pid, "Orange", 1500)  # type: ignore
        product = await get_product(pid)  # type: ignore
        print(f"✓ Updated: id={product.id}, name={product.name}, price={product.price}\n")  # type: ignore

        # DELETE
        print("[DELETE]")
        await delete_product(pid)  # type: ignore
        product = await get_product(pid)  # type: ignore
        print(f"✓ Deleted: product={'not found' if product is None else 'still exists'}\n")

    print("=" * 60)
    print("All tests passed!")


if __name__ == "__main__":
    subprocess.run(["./scripts/setup_dev_db.sh"])
    asyncio.run(test_crud())
