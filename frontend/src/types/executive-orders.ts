/**
 * Executive Order related types
 */

// Status of an executive order
export type OrderStatus = 'Active' | 'Revoked' | 'Superseded' | 'Amended';

// Executive Order model
export interface ExecutiveOrder {
  id: string;
  number: string;
  title: string;
  presidentName: string;
  signedDate: string;
  federalRegisterUrl: string;
  status: OrderStatus;
  summary: string;
  fullText?: string;
  revokedBy?: string;
  amendedBy?: string[];
  supersededBy?: string;
  relatedOrders?: string[];
  policyAreas?: string[];
  citations?: string[];
  createdAt: string;
  updatedAt: string;
}

// Response containing a list of executive orders
export interface OrdersResponse {
  orders: ExecutiveOrder[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

// Response containing a single executive order
export interface OrderResponse {
  order: ExecutiveOrder;
}

// Base filter state for executive orders search
export interface FilterState {
  president?: string;
  status?: OrderStatus;
  startDate?: string;
  endDate?: string;
  policyArea?: string;
  search?: string;
  sortBy?: 'date' | 'number' | 'title';
  sortDirection?: 'asc' | 'desc';
  page?: number;
  pageSize?: number;
}

// Executive order statistics
export interface OrderStats {
  totalOrders: number;
  byPresident: Record<string, number>;
  byStatus: Record<OrderStatus, number>;
  byYear: Record<string, number>;
  byPolicyArea: Record<string, number>;
}
