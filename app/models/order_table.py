from sqlalchemy import Column, String, ForeignKey, Numeric, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import ENUM
from app.core.database import Base

order_status_enum = ENUM(
    "CREATED",
    "IN_PROGRESS",
    "COMPLETED",
    name="order_status_enum",
    create_type=True
)

class OrderTable(Base):
    __tablename__ = "order_table"

    order_id = Column(String, primary_key=True, index=True)

    user_id = Column(
        String,
        ForeignKey("user_table.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    client_name = Column(String, nullable=False)

    total_order_amount = Column(Numeric(14, 2), nullable=False, default=0)

    status = Column(order_status_enum, nullable=False, server_default="CREATED")

    ordered_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )

    invoice_generated_at = Column(TIMESTAMP(timezone=True), nullable=True)
    paid_at = Column(TIMESTAMP(timezone=True), nullable=True)
