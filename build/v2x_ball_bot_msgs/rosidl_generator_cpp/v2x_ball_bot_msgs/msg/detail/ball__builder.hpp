// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from v2x_ball_bot_msgs:msg/Ball.idl
// generated code does not contain a copyright notice

#ifndef V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL__BUILDER_HPP_
#define V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "v2x_ball_bot_msgs/msg/detail/ball__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace v2x_ball_bot_msgs
{

namespace msg
{

namespace builder
{

class Init_Ball_is_static
{
public:
  explicit Init_Ball_is_static(::v2x_ball_bot_msgs::msg::Ball & msg)
  : msg_(msg)
  {}
  ::v2x_ball_bot_msgs::msg::Ball is_static(::v2x_ball_bot_msgs::msg::Ball::_is_static_type arg)
  {
    msg_.is_static = std::move(arg);
    return std::move(msg_);
  }

private:
  ::v2x_ball_bot_msgs::msg::Ball msg_;
};

class Init_Ball_score
{
public:
  explicit Init_Ball_score(::v2x_ball_bot_msgs::msg::Ball & msg)
  : msg_(msg)
  {}
  Init_Ball_is_static score(::v2x_ball_bot_msgs::msg::Ball::_score_type arg)
  {
    msg_.score = std::move(arg);
    return Init_Ball_is_static(msg_);
  }

private:
  ::v2x_ball_bot_msgs::msg::Ball msg_;
};

class Init_Ball_z
{
public:
  explicit Init_Ball_z(::v2x_ball_bot_msgs::msg::Ball & msg)
  : msg_(msg)
  {}
  Init_Ball_score z(::v2x_ball_bot_msgs::msg::Ball::_z_type arg)
  {
    msg_.z = std::move(arg);
    return Init_Ball_score(msg_);
  }

private:
  ::v2x_ball_bot_msgs::msg::Ball msg_;
};

class Init_Ball_y
{
public:
  explicit Init_Ball_y(::v2x_ball_bot_msgs::msg::Ball & msg)
  : msg_(msg)
  {}
  Init_Ball_z y(::v2x_ball_bot_msgs::msg::Ball::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_Ball_z(msg_);
  }

private:
  ::v2x_ball_bot_msgs::msg::Ball msg_;
};

class Init_Ball_x
{
public:
  explicit Init_Ball_x(::v2x_ball_bot_msgs::msg::Ball & msg)
  : msg_(msg)
  {}
  Init_Ball_y x(::v2x_ball_bot_msgs::msg::Ball::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_Ball_y(msg_);
  }

private:
  ::v2x_ball_bot_msgs::msg::Ball msg_;
};

class Init_Ball_id
{
public:
  explicit Init_Ball_id(::v2x_ball_bot_msgs::msg::Ball & msg)
  : msg_(msg)
  {}
  Init_Ball_x id(::v2x_ball_bot_msgs::msg::Ball::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_Ball_x(msg_);
  }

private:
  ::v2x_ball_bot_msgs::msg::Ball msg_;
};

class Init_Ball_stamp
{
public:
  Init_Ball_stamp()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Ball_id stamp(::v2x_ball_bot_msgs::msg::Ball::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return Init_Ball_id(msg_);
  }

private:
  ::v2x_ball_bot_msgs::msg::Ball msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::v2x_ball_bot_msgs::msg::Ball>()
{
  return v2x_ball_bot_msgs::msg::builder::Init_Ball_stamp();
}

}  // namespace v2x_ball_bot_msgs

#endif  // V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL__BUILDER_HPP_
