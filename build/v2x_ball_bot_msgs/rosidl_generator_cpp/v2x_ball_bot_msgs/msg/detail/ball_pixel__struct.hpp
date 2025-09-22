// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from v2x_ball_bot_msgs:msg/BallPixel.idl
// generated code does not contain a copyright notice

#ifndef V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_PIXEL__STRUCT_HPP_
#define V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_PIXEL__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__v2x_ball_bot_msgs__msg__BallPixel __attribute__((deprecated))
#else
# define DEPRECATED__v2x_ball_bot_msgs__msg__BallPixel __declspec(deprecated)
#endif

namespace v2x_ball_bot_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct BallPixel_
{
  using Type = BallPixel_<ContainerAllocator>;

  explicit BallPixel_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->u = 0l;
      this->v = 0l;
    }
  }

  explicit BallPixel_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->u = 0l;
      this->v = 0l;
    }
  }

  // field types and members
  using _u_type =
    int32_t;
  _u_type u;
  using _v_type =
    int32_t;
  _v_type v;

  // setters for named parameter idiom
  Type & set__u(
    const int32_t & _arg)
  {
    this->u = _arg;
    return *this;
  }
  Type & set__v(
    const int32_t & _arg)
  {
    this->v = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    v2x_ball_bot_msgs::msg::BallPixel_<ContainerAllocator> *;
  using ConstRawPtr =
    const v2x_ball_bot_msgs::msg::BallPixel_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<v2x_ball_bot_msgs::msg::BallPixel_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<v2x_ball_bot_msgs::msg::BallPixel_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      v2x_ball_bot_msgs::msg::BallPixel_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<v2x_ball_bot_msgs::msg::BallPixel_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      v2x_ball_bot_msgs::msg::BallPixel_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<v2x_ball_bot_msgs::msg::BallPixel_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<v2x_ball_bot_msgs::msg::BallPixel_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<v2x_ball_bot_msgs::msg::BallPixel_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__v2x_ball_bot_msgs__msg__BallPixel
    std::shared_ptr<v2x_ball_bot_msgs::msg::BallPixel_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__v2x_ball_bot_msgs__msg__BallPixel
    std::shared_ptr<v2x_ball_bot_msgs::msg::BallPixel_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const BallPixel_ & other) const
  {
    if (this->u != other.u) {
      return false;
    }
    if (this->v != other.v) {
      return false;
    }
    return true;
  }
  bool operator!=(const BallPixel_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct BallPixel_

// alias to use template instance with default allocator
using BallPixel =
  v2x_ball_bot_msgs::msg::BallPixel_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace v2x_ball_bot_msgs

#endif  // V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_PIXEL__STRUCT_HPP_
