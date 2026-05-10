import "@testing-library/jest-dom/vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";
import { OrderSuccessPage } from "../pages/OrderSuccessPage";

describe("OrderSuccessPage", () => {
  it("renders order id from query string", () => {
    render(
      <MemoryRouter initialEntries={["/order-success?orderId=ord_abc"]}>
        <OrderSuccessPage />
      </MemoryRouter>,
    );

    expect(screen.getByText(/ord_abc/)).toBeInTheDocument();
  });
});
